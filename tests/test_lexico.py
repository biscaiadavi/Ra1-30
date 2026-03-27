# Testes do analisador léxico (AFD) — entradas válidas e inválidas.

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import unittest

from lexico import ErroLexico, parseExpressao


class TestLexicoValido(unittest.TestCase):
    def test_simples(self) -> None:
        self.assertEqual(parseExpressao("(3.14 2.0 +)"), ["(", "3.14", "2.0", "+", ")"])

    def test_operadores(self) -> None:
        self.assertEqual(
            parseExpressao("(A B //)"),
            ["(", "A", "B", "//", ")"],
        )
        self.assertEqual(parseExpressao("(X Y %)"), ["(", "X", "Y", "%", ")"])
        self.assertEqual(parseExpressao("(1 2 ^)"), ["(", "1", "2", "^", ")"])

    def test_res_mem(self) -> None:
        self.assertEqual(parseExpressao("(5 RES)"), ["(", "5", "RES", ")"])
        self.assertEqual(parseExpressao("(10.5 CONTADOR)"), ["(", "10.5", "CONTADOR", ")"])
        self.assertEqual(parseExpressao("(MEM)"), ["(", "MEM", ")"])

    def test_aninhado(self) -> None:
        t = parseExpressao("((1.0 2.0 +) (3.0 4.0 *) /)")
        self.assertEqual(
            t,
            [
                "(",
                "(",
                "1.0",
                "2.0",
                "+",
                ")",
                "(",
                "3.0",
                "4.0",
                "*",
                ")",
                "/",
                ")",
            ],
        )

    def test_interface_tokens_ref(self) -> None:
        buf: list[str] = []
        parseExpressao("(1 2 +)", buf)
        self.assertEqual(buf, ["(", "1", "2", "+", ")"])

    def test_interface_segundo_parametro_linha_vazia_limpa_lista(self) -> None:
        buf: list[str] = ["lixo"]
        self.assertEqual(parseExpressao("   ", buf), [])
        self.assertEqual(buf, [])


class TestLexicoInvalido(unittest.TestCase):
    def test_numero_malformado(self) -> None:
        with self.assertRaises(ErroLexico):
            parseExpressao("(3.14.5 2.0 +)")
        with self.assertRaises(ErroLexico):
            parseExpressao("(3,14 2.0 +)")

    def test_token_invalido(self) -> None:
        with self.assertRaises(ErroLexico):
            parseExpressao("(3.14 2.0 &)")


if __name__ == "__main__":
    unittest.main()
