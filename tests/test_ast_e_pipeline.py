import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import unittest

from ast_parser import ErroSintaxe, parse_linha_tokens
from gerador_arm import ErroGeracao
from lexico import parseExpressao
from main import contextoAtivo, executarExpressao, gerarAssembly, iniciarContextoCompilacao


class TestAst(unittest.TestCase):
    def test_parenteses_incompletos(self) -> None:
        t = parseExpressao("(1 2 +")
        with self.assertRaises(ErroSintaxe):
            parse_linha_tokens(t)

    def test_parse_completo(self) -> None:
        ast = parse_linha_tokens(parseExpressao("((1.0 2.0 +) (3.0 4.0 *) /)"))
        self.assertEqual(ast[0], "bin")


class TestPipeline(unittest.TestCase):
    def test_gera_assembly_nao_vazio(self) -> None:
        iniciarContextoCompilacao()
        ctx = contextoAtivo()
        linha = "((2.0 3.0 +) (4.0 1.0 -) *)"
        executarExpressao(parseExpressao(linha), ctx)
        out: list[str] = []
        gerarAssembly(parseExpressao(linha), out)
        self.assertTrue(any("vadd.f64" in x for x in out))
        self.assertTrue(any("_start:" in x for x in out))

    def test_res_invalido_linha_inicial(self) -> None:
        """(N RES) na primeira linha: não há N linhas anteriores no histórico."""
        iniciarContextoCompilacao()
        ctx = contextoAtivo()
        linha = "(1 RES)"
        executarExpressao(parseExpressao(linha), ctx)
        out: list[str] = []
        with self.assertRaises(ErroGeracao):
            gerarAssembly(parseExpressao(linha), out)

    def test_expoente_negativo_gera_rotulo_pow_neg_err(self) -> None:
        """Expoente negativo (ex.: 2^(1-4)) deve emitir desvio para pow_neg_err no Assembly."""
        iniciarContextoCompilacao()
        ctx = contextoAtivo()
        linha = "(2.0 (1.0 4.0 -) ^)"
        executarExpressao(parseExpressao(linha), ctx)
        out: list[str] = []
        gerarAssembly(parseExpressao(linha), out)
        self.assertTrue(any("pow_neg_err" in x for x in out))

    def test_divisao_zero_divisao_inteira(self) -> None:
        iniciarContextoCompilacao()
        ctx = contextoAtivo()
        linha = "(1.0 0.0 //)"
        executarExpressao(parseExpressao(linha), ctx)
        out: list[str] = []
        gerarAssembly(parseExpressao(linha), out)
        self.assertTrue(any("divzero_die" in x for x in out))
        self.assertTrue(any("beq divzero_die" in x for x in out))

    def test_divisao_zero_resto(self) -> None:
        iniciarContextoCompilacao()
        ctx = contextoAtivo()
        linha = "(1.0 0.0 %)"
        executarExpressao(parseExpressao(linha), ctx)
        out: list[str] = []
        gerarAssembly(parseExpressao(linha), out)
        self.assertTrue(any("divzero_die" in x for x in out))
        self.assertTrue(any("beq divzero_die" in x for x in out))


if __name__ == "__main__":
    unittest.main()
