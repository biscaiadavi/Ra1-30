#!/usr/bin/env python3
# rpn_fase1 — Repositório: https://github.com/Neskrux/Ra1-30
# Integrantes (Bruno Sandoval, Davi Biscai) 
# Integrantes :  @Neskrux, @biscaiadavi]
# Grupo (Canvas): [RA1 30]
# PUCPR / Construção de Interpretadores / Professor: [Frank Coelho]

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set

from ast_parser import ErroSintaxe, coletar_literais, coletar_memorias, parse_linha_tokens
from gerador_arm import ErroGeracao, gerarAssembly as _gerarAssembly_interno
from lexico import ErroLexico, parseExpressao

_CTX_ATIVO: ContextoExecucao | None = None


@dataclass
class ContextoExecucao:
    """Estado simbólico da “execução”: ASTs por linha, memórias e literais para o Assembly."""

    asts: list = field(default_factory=list)
    memorias: Set[str] = field(default_factory=set)
    literais: Set[str] = field(default_factory=set)
    resumos_linha: List[str] = field(default_factory=list)


def lerArquivo(nomeArquivo: str, linhas: List[str]) -> None:
    """Lê o arquivo de teste para o vetor linhas (uma string por linha, sem \\n final)."""
    linhas.clear()
    p = Path(nomeArquivo)
    if not p.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {nomeArquivo}")
    texto = p.read_text(encoding="utf-8")
    for raw in texto.splitlines():
        linhas.append(raw.rstrip("\r"))


def iniciarContextoCompilacao() -> None:
    """Inicia um novo contexto (um arquivo de teste / uma execução completa)."""
    global _CTX_ATIVO
    _CTX_ATIVO = ContextoExecucao()


def contextoAtivo() -> ContextoExecucao:
    if _CTX_ATIVO is None:
        raise RuntimeError("Contexto não iniciado: chame iniciarContextoCompilacao() antes.")
    return _CTX_ATIVO


def executarExpressao(linha_tokens: List[str], estado: ContextoExecucao) -> None:
    """
    Constrói a AST da linha, atualiza conjuntos de memória/literais e o histórico simbólico.
    Não avalia operações aritméticas da linguagem em Python — apenas estrutura para o Assembly.
    """
    ast = parse_linha_tokens(linha_tokens)
    estado.asts.append(ast)
    coletar_memorias(ast, estado.memorias)
    coletar_literais(ast, estado.literais)
    n = len(estado.asts)
    estado.resumos_linha.append(
        f"Linha {n}: expressão aceita; resultado será gravado em hist[{n - 1}] "
        f"e refletido no display HEX (0xFF200020) no CPUlator após a execução da linha."
    )


def gerarAssembly(_tokens_: List[str], codigoAssembly: List[str]) -> None:
    """
    Recebe o vetor de tokens (última linha ou vazio) e preenche codigoAssembly com o programa ARM completo.
    O estado simbólico vem das chamadas anteriores a executarExpressao no mesmo contexto iniciado por iniciarContextoCompilacao().
    """
    _ = _tokens_
    estado = contextoAtivo()
    _gerarAssembly_interno(estado.asts, estado.memorias, estado.literais, codigoAssembly)


def exibirResultados(resultados: List[str]) -> None:
    """Exibe resumo textual por linha (sem calcular em Python o valor das expressões)."""
    print("=== Resumo da compilação (valores finais apenas no ARM / CPUlator) ===")
    for r in resultados:
        print(r)


def _gravar_tokens(linhas_tokens: List[List[str]], caminho: Path) -> None:
    caminho.write_text(json.dumps(linhas_tokens, ensure_ascii=False, indent=2), encoding="utf-8")


def _gravar_asm(linhas: List[str], caminho: Path) -> None:
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def main(argv: List[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    if len(argv) != 2:
        print("Uso: python main.py <arquivo_teste.txt>", file=sys.stderr)
        return 2
    nome = argv[1]
    linhas_arquivo: List[str] = []
    try:
        lerArquivo(nome, linhas_arquivo)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    iniciarContextoCompilacao()
    estado = contextoAtivo()
    linhas_tokens: List[List[str]] = []
    base_dir = Path(__file__).resolve().parent

    for texto in linhas_arquivo:
        # Permite comentários com '#': ignora linha inteira comentada ou trecho após '#'.
        texto_limpo = texto.split("#", 1)[0].strip()
        if not texto_limpo:
            continue
        toks = parseExpressao(texto_limpo)
        if not toks:
            continue
        linhas_tokens.append(toks)
        try:
            executarExpressao(toks, estado)
        except (ErroSintaxe, ErroLexico) as e:
            print(f"Erro na linha do arquivo ({texto!r}): {e}", file=sys.stderr)
            return 1

    if not estado.asts:
        print("Nenhuma expressão válida no arquivo.", file=sys.stderr)
        return 1

    codigo: List[str] = []
    try:
        gerarAssembly(linhas_tokens[-1] if linhas_tokens else [], codigo)
    except ErroGeracao as e:
        print(f"Erro na geração de Assembly: {e}", file=sys.stderr)
        return 1

    _gravar_tokens(linhas_tokens, base_dir / "tokens_ultima_execucao.txt")
    _gravar_asm(codigo, base_dir / "saida_arm.s")

    exibirResultados(estado.resumos_linha)
    print()
    print(f"Tokens salvos em: {base_dir / 'tokens_ultima_execucao.txt'}")
    print(f"Assembly salvo em: {base_dir / 'saida_arm.s'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
