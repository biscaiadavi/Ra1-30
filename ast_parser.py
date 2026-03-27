# Parser recursivo de expressões RPN parentetizadas (sem avaliar aritmética da linguagem).
# Integrantes (Bruno Sandoval, Davi Biscai) 
# Integrantes :  @Neskrux, @biscaiadavi
# Grupo (Canvas): [RA1 30]
# PUCPR / Construção de Interpretadores / Professor: [Frank Coelho]

from __future__ import annotations

from typing import List, Tuple, Union

OPS = frozenset({"+", "-", "*", "/", "//", "%", "^"})

AstNode = Union[
    Tuple[str, str],
    Tuple[str, str, "AstNode", "AstNode"],
    Tuple[str, str, "AstNode"],
    Tuple[str, int],
]


class ErroSintaxe(Exception):
    pass


def _eh_ident_mem(s: str) -> bool:
    return bool(s) and all("A" <= c <= "Z" for c in s)


def _eh_natural(s: str) -> bool:
    return bool(s) and s.isdigit()


def _eh_literal_real(s: str) -> bool:
    if s == ".":
        return False
    p = 0
    for ch in s:
        if ch == ".":
            p += 1
            if p > 1:
                return False
        elif not ch.isdigit():
            return False
    return True


def parse_atom(tokens: List[str], i: int) -> Tuple[AstNode, int]:
    if i >= len(tokens):
        raise ErroSintaxe("Operando ausente")
    if tokens[i] == "(":
        return parse_paren_expr(tokens, i)
    if _eh_literal_real(tokens[i]):
        return ("num", tokens[i]), i + 1
    raise ErroSintaxe(f"Operando inválido: {tokens[i]!r}")


def parse_paren_expr(tokens: List[str], i: int) -> Tuple[AstNode, int]:
    if i >= len(tokens) or tokens[i] != "(":
        raise ErroSintaxe("Esperado '('")
    i += 1
    if i >= len(tokens):
        raise ErroSintaxe("Expressão incompleta após '('")

    if i + 1 < len(tokens) and _eh_ident_mem(tokens[i]) and tokens[i + 1] == ")":
        nome = tokens[i]
        if nome == "RES":
            raise ErroSintaxe("(RES) não é referência de memória válida")
        return ("load", nome), i + 2

    if (
        _eh_natural(tokens[i])
        and i + 2 < len(tokens)
        and tokens[i + 1] == "RES"
        and tokens[i + 2] == ")"
    ):
        return ("res", int(tokens[i])), i + 3

    primeiro, i = parse_atom(tokens, i)
    if i >= len(tokens):
        raise ErroSintaxe("Expressão incompleta")

    if tokens[i] == ")":
        raise ErroSintaxe("Falta operador ou nome de memória")

    if _eh_ident_mem(tokens[i]) and tokens[i] != "RES":
        if i + 1 < len(tokens) and tokens[i + 1] == ")":
            return ("store", tokens[i], primeiro), i + 2
        raise ErroSintaxe("Esperado ')' após nome da memória")

    segundo, i = parse_atom(tokens, i)
    if i >= len(tokens) or tokens[i] not in OPS:
        raise ErroSintaxe("Operador aritmético esperado")
    op = tokens[i]
    i += 1
    if i >= len(tokens) or tokens[i] != ")":
        raise ErroSintaxe("Esperado ')' final")
    return ("bin", op, primeiro, segundo), i + 1


def parse_linha_tokens(tokens: List[str]) -> AstNode:
    ast, j = parse_paren_expr(tokens, 0)
    if j != len(tokens):
        raise ErroSintaxe(f"Sobraram tokens após a expressão (índice {j})")
    return ast


def coletar_literais(ast: AstNode, dest: set[str]) -> None:
    t = ast[0]
    if t == "num":
        dest.add(ast[1])
        return
    if t in ("load", "res"):
        return
    if t == "store":
        coletar_literais(ast[2], dest)
        return
    if t == "bin":
        coletar_literais(ast[2], dest)
        coletar_literais(ast[3], dest)
        return


def coletar_memorias(ast: AstNode, dest: set[str]) -> None:
    t = ast[0]
    if t == "num":
        return
    if t == "load":
        dest.add(ast[1])
        return
    if t == "res":
        return
    if t == "store":
        dest.add(ast[1])
        coletar_memorias(ast[2], dest)
        return
    if t == "bin":
        coletar_memorias(ast[2], dest)
        coletar_memorias(ast[3], dest)
        return
