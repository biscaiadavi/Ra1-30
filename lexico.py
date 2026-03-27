# Lexico — AFD: cada estado é uma função (sem regex na análise léxica).
# Integrantes (Bruno Sandoval, Davi Biscai) 
# Integrantes :  @Neskrux, @biscaiadavi]
# Grupo (Canvas): [RA1 30]
# PUCPR / Construção de Interpretadores / Professor: [Frank Coelho]
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple


class ErroLexico(Exception):
    pass


@dataclass
class _CtxLex:
    linha: str
    tokens: List[str] = field(default_factory=list)
    buffer: str = ""

    def emitir_token(self, t: str) -> None:
        if t:
            self.tokens.append(t)

    def limpar_buffer(self) -> None:
        self.buffer = ""


# Tipo: (caractere ou '\0' no fim, índice atual) -> (próximo_estado, novo_índice)
EstadoFn = Callable[[str, int, _CtxLex], Tuple[Callable[..., Tuple], int]]


def _fim_ou_espaco(c: str) -> bool:
    return c in " \t\n\r\0"


def _eh_digito(c: str) -> bool:
    return len(c) == 1 and c.isdigit()


def _eh_maiuscula(c: str) -> bool:
    return len(c) == 1 and "A" <= c <= "Z"


def estado_inicial(c: str, i: int, ctx: _CtxLex) -> Tuple[EstadoFn, int]:
    if c in " \t\n\r":
        return estado_inicial, i + 1
    if c == "\0":
        return estado_inicial, i + 1
    if c == "(":
        ctx.emitir_token("(")
        return estado_inicial, i + 1
    if c == ")":
        ctx.emitir_token(")")
        return estado_inicial, i + 1
    if c == "+":
        ctx.emitir_token("+")
        return estado_inicial, i + 1
    if c == "-":
        ctx.emitir_token("-")
        return estado_inicial, i + 1
    if c == "*":
        ctx.emitir_token("*")
        return estado_inicial, i + 1
    if c == "%":
        ctx.emitir_token("%")
        return estado_inicial, i + 1
    if c == "^":
        ctx.emitir_token("^")
        return estado_inicial, i + 1
    if c == "/":
        return estado_barra, i + 1
    if _eh_digito(c) or c == ".":
        ctx.buffer = c
        return estado_numero, i + 1
    if _eh_maiuscula(c):
        ctx.buffer = c
        return estado_identificador, i + 1
    raise ErroLexico(f"Caractere inválido na posição {i}: {c!r}")


def estado_barra(c: str, i: int, ctx: _CtxLex) -> Tuple[EstadoFn, int]:
    if c == "/":
        ctx.emitir_token("//")
        return estado_inicial, i + 1
    ctx.emitir_token("/")
    if c == "\0":
        return estado_inicial, i + 1
    return estado_inicial, i


def estado_numero(c: str, i: int, ctx: _CtxLex) -> Tuple[EstadoFn, int]:
    if _eh_digito(c):
        ctx.buffer += c
        return estado_numero, i + 1
    if c == ".":
        if "." in ctx.buffer:
            raise ErroLexico("Número malformado: mais de um ponto decimal")
        ctx.buffer += c
        return estado_apos_ponto, i + 1
    if _fim_ou_espaco(c) or c in "()+-*/%^":
        if ctx.buffer == "." or ctx.buffer == "-." or ctx.buffer.endswith("-"):
            raise ErroLexico(f"Número malformado: {ctx.buffer!r}")
        if ctx.buffer.endswith("."):
            raise ErroLexico(f"Número malformado (ponto sem parte fracionária): {ctx.buffer!r}")
        ctx.emitir_token(ctx.buffer)
        ctx.limpar_buffer()
        if c == "\0" or c in " \t\n\r":
            return estado_inicial, i + 1
        return estado_inicial, i
    raise ErroLexico(f"Número malformado na posição {i}: {c!r}")


def estado_apos_ponto(c: str, i: int, ctx: _CtxLex) -> Tuple[EstadoFn, int]:
    if _eh_digito(c):
        ctx.buffer += c
        return estado_frac, i + 1
    raise ErroLexico("Número malformado: '.' sem dígitos após")


def estado_frac(c: str, i: int, ctx: _CtxLex) -> Tuple[EstadoFn, int]:
    if _eh_digito(c):
        ctx.buffer += c
        return estado_frac, i + 1
    if c == ".":
        raise ErroLexico("Número malformado: segundo ponto decimal")
    if _fim_ou_espaco(c) or c in "()+-*/%^":
        ctx.emitir_token(ctx.buffer)
        ctx.limpar_buffer()
        if c == "\0" or c in " \t\n\r":
            return estado_inicial, i + 1
        return estado_inicial, i
    raise ErroLexico(f"Número malformado na posição {i}: {c!r}")


def estado_identificador(c: str, i: int, ctx: _CtxLex) -> Tuple[EstadoFn, int]:
    if _eh_maiuscula(c):
        ctx.buffer += c
        return estado_identificador, i + 1
    if _fim_ou_espaco(c) or c in "()+-*/%^" or c == "/":
        ctx.emitir_token(ctx.buffer)
        ctx.limpar_buffer()
        if c == "\0" or c in " \t\n\r":
            return estado_inicial, i + 1
        return estado_inicial, i
    raise ErroLexico(f"Identificador inválido (apenas A–Z) na posição {i}: {c!r}")


def _executar_afd(linha: str) -> List[str]:
    ctx = _CtxLex(linha=linha)
    estado: EstadoFn = estado_inicial
    i = 0
    n = len(linha)
    while i <= n:
        c = linha[i] if i < n else "\0"
        estado, i = estado(c, i, ctx)
    return ctx.tokens


def parseExpressao(linha: str, _tokens_: Optional[List[str]] = None) -> List[str]:
    """
    Analisa uma linha (análise léxica via AFD) e devolve a lista de tokens.
    Se _tokens_ for fornecido, limpa e preenche esse vetor (interface pedida).
    """
    s = linha.strip()
    if not s:
        if _tokens_ is not None:
            _tokens_.clear()
        return []
    toks = _executar_afd(s)
    if _tokens_ is not None:
        _tokens_.clear()
        _tokens_.extend(toks)
    return toks
