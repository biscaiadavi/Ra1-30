# Fase 1 — Analisador léxico (AFD) e gerador de Assembly ARMv7 (DE1-SoC / CPUlator)

## Repositório

- **GitHub:** [Neskrux/Ra1-30](https://github.com/Neskrux/Ra1-30)
- **Clone (HTTPS):** `git clone https://github.com/Neskrux/Ra1-30.git`


```bash
git init
git branch -M main
git remote add origin https://github.com/Neskrux/Ra1-30.git
git add .
git commit -m "Fase 1: léxico AFD, AST, gerador ARMv7 e testes"
git push -u origin main
```

## Instituição, disciplina e docente

- **Instituição:** [PUCPR]
- **Disciplina:** [Construção de Interpretadores]
- **Professor:** [Frank Coelho]
- **Alunos:** [Bruno Sandoval, Davi Biscaia]

## Grupo e integrantes (ordem alfabética + usuário GitHub)

- **Nome do grupo (Canvas):** [RA1 30]
- [Nome Completo](https://github.com/USUARIO) — ` @Neskrux, @biscaiadavi`

## Objetivo

Programa em **Python** que:

1. Lê um arquivo de expressões em RPN parentetizada (uma expressão por linha).
2. Realiza **análise léxica** com **autômato finito determinístico** (cada estado é uma função; **sem regex** na léxica).
3. Constrói a AST da linha (**sem avaliar** em Python as operações `+ - * / // % ^` da linguagem).
4. Gera **Assembly ARMv7** com **VFP (IEEE 754 dupla precisão)** para o simulador **CPUlator — ARMv7 DE1-SoC (v16.1)**.
5. Grava `tokens_ultima_execucao.txt` (JSON com os tokens da última execução) e `saida_arm.s` (último Assembly gerado).

Os **cálculos** ocorrem apenas no **Assembly** gerado. A saída numérica formatada no console não replica o valor em ponto flutuante (evita `eval` / operações da linguagem em Python); o resultado deve ser verificado no **CPUlator** (registrador `d0`, memória `hist`, display **HEX3–HEX0** em `0xFF200020`).

### Divisão real (`/`) vs. divisão inteira (`//`) e resto (`%`)

- **Divisão real** usa instruções VFP em precisão dupla: `vdiv.f64` sobre valores IEEE 754 (`f64`).
- **Divisão inteira** (`//`) e **resto** (`%`) convertem os operandos de `f64` para inteiro com sinal (`vcvt.s32.f64`) e usam uma rotina local `idiv_s32` no próprio Assembly gerado (compatível com CPUlator). O resultado volta a `f64` para manter o fluxo da pilha RPN.

### Divisão inteira com operandos negativos

A conversão `vcvt.s32.f64` segue a regra usual de **truncamento em direção a zero** (como conversão de ponto flutuante para inteiro em C). Em seguida, a rotina `idiv_s32` aplica divisão inteira com sinal em ARM sem depender de bibliotecas externas. Essa combinação define a semântica de `//` e `%` nesta fase; valores nos extremos do intervalo de `s32` podem sofrer saturação ou comportamento indefinido se o `double` estiver fora do range representável em 32 bits.

## Requisitos

- Python 3.10+ (recomendado).

## Execução

Na pasta do projeto:

```bash
python main.py teste1.txt
```

Equivalente ao `./programa teste1.txt` após tornar o script executável em Unix.

Saídas:

- `tokens_ultima_execucao.txt` — lista de listas de tokens (última execução).
- `saida_arm.s` — programa Assembly correspondente **exatamente** ao último arquivo processado.

Formato de `tokens_ultima_execucao.txt`:
- Arquivo em **JSON**.
- Estrutura: array de linhas, em que cada linha é um array de tokens.
- Exemplo simplificado: `[["(", "2.0", "3.0", "+", ")"], ...]`.

## Testes

```bash
python -m unittest discover -s tests -v
```

Inclui testes do **léxico** (válidos e inválidos), **parser** e testes de **pipeline** (geração de Assembly, `RES` inválido, expoente negativo em `^`, divisão por zero em `//` e `%`).

## Uso no CPUlator

1. Abra [CPUlator](https://cpulator.01xz.net/?sys=arm-de1soc) e selecione o sistema **ARMv7 DE1-SoC**.
2. Copie o conteúdo de `saida_arm.s` para o editor (ou carregue o arquivo).
3. **Compile and Load (F5)**.
4. Execute (**Continue**). O programa entra em laço final `halt_loop` após processar todas as linhas.
5. Observe o **display de 7 segmentos** (HEX) e/ou inspecione `hist` e variáveis `mem_*` na janela de memória.

## Funções principais (contrato da disciplina)

| Função | Módulo | Descrição |
|--------|--------|-----------|
| `parseExpressao` | `lexico.py` | Léxico AFD → vetor de tokens. Aceita assinatura `parseExpressao(linha)` ou `parseExpressao(linha, _tokens_)`: se `_tokens_` for uma lista, ela é limpa e preenchida com os mesmos tokens retornados (interface por referência). |
| `executarExpressao` | `main.py` | Monta AST e estado simbólico (memórias/literais) por linha. |
| `gerarAssembly` | `main.py` | Preenche `codigoAssembly` com o programa ARM (usa contexto da execução atual). |
| `exibirResultados` | `main.py` | Imprime resumo por linha (sem calcular expressões em Python). |
| `lerArquivo` | `main.py` | Lê linhas do arquivo de teste. |

Fluxo interno: `iniciarContextoCompilacao()` antes de processar um arquivo; em seguida, para cada linha, `parseExpressao` → `executarExpressao`; ao final, `gerarAssembly`.

## Arquivos de teste

- `teste1.txt`, `teste2.txt`, `teste3.txt` — cada um com **12 linhas**, cobrindo operadores `+ - * / // % ^`, comandos `(N RES)`, `(V MEM)`, `(MEM)` e aninhamento.
- Os arquivos de teste aceitam comentários com `#` (linha inteira ou comentário ao final da linha), ignorados durante a leitura.

## Estrutura do repositório

```
main.py              # Ponto de entrada, orquestração, funções pedidas
lexico.py            # AFD (estados como funções)
ast_parser.py        # AST a partir dos tokens
gerador_arm.py       # Emissão ARMv7 + VFP
tests/               # Testes unitários
teste1.txt …         # Entradas de exemplo
saida_arm.s          # Último Assembly (regenerado ao rodar main.py)
tokens_ultima_execucao.txt
```

Preencha os campos `[PREENCHER]` nos cabeçalhos de `main.py` / `lexico.py` e neste README antes da entrega.
