# Analisador de Testes A/B — Méliuz

Solução reutilizável para análise de testes A/B de cashback. Basta abrir o Claude Code na pasta do projeto e fazer a pergunta em linguagem natural.

## Como usar

1. Clone o repositório
2. Abra o **Claude Code desktop** na pasta do projeto
3. Digite a pergunta:
   > "Dado esse teste A/B, qual variante de cashback devemos escalar pra 100% do tráfego?"
4. O Claude vai listar os datasets disponíveis em `datasets/` e perguntar quais analisar
5. Escolha os datasets e depois escolha o **modo de análise** (veja abaixo)

## Modos de análise

Após selecionar os datasets, o Claude perguntará como você prefere rodar a análise:

### Modo [1] — Apenas Claude Code

Sem dependências externas, funciona em qualquer máquina com Claude Code instalado.

- Não requer Python nem Node.js
- Durante a execução podem aparecer pedidos de permissão — clique em **"Sempre permitir"** ou **"Permitir"** para continuar
- **Pode levar até 15 minutos** dependendo do tamanho dos datasets
- **Consome mais créditos do Claude** do que o Modo [2], pois todo o processamento é feito pelo modelo

### Modo [2] — Python + Node.js _(recomendado)_

Análise mais rápida via scripts otimizados. Requer Python e Node.js instalados na máquina.

- Significativamente mais rápido que o Modo [1]
- **Consome menos créditos do Claude**, pois o processamento pesado é delegado aos scripts
- Requer as dependências abaixo instaladas:

```bash
# Instalar dependências Python
pip install pandas scipy

# Node.js é necessário para o upload ao Google Sheets via MCP
```

Para rodar manualmente (sem o Claude Code):

```bash
python analyze.py datasets/dataset_01_parceiroA.csv
```

## O que é gerado

| Arquivo | Descrição |
|---|---|
| `reports/relatorio_<Parceiro>.md` | Relatório detalhado por teste, apresentável para um gestor |
| `resultados.csv` | Consolidado de todos os testes analisados |

Os resultados são enviados automaticamente para o Google Sheets após a gravação do `resultados.csv`.

## Estrutura do projeto

```
├── CLAUDE.md                        # Instruções do agente
├── README.md
├── analyze.py                       # Script Python (Modo [2])
├── datasets/                        # CSVs dos testes A/B
│   ├── dataset_01_parceiroA.csv
│   ├── dataset_02_parceiroB.csv
│   └── dataset_03_parceiroC.csv
├── reports/                         # Relatórios gerados pelo agente
├── resultados.csv                   # Planilha consolidada
└── scripts/
    └── upload_sheets.log            # Log dos uploads ao Google Sheets
```
