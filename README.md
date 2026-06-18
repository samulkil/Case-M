# Analisador de Testes — Méliuz

Solução reutilizável para análise de testes de cashback. Basta abrir o Claude Code na pasta do projeto e fazer a pergunta em linguagem natural.

## Como usar

1. Clone o repositório
2. Abra o **Claude Code desktop** na pasta do projeto
3. Digite a pergunta ou uma variante de:
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

### Modo [2] — Python _(recomendado)_

Análise mais rápida via scripts otimizados. Requer Python e uma dependência instalado na máquina.

- Significativamente mais rápido que o Modo [1]
- **Consome menos créditos do Claude**, pois o processamento pesado é delegado aos scripts
- O upload ao Google Sheets **não** é feito pelos scripts Python: assim como no Modo [1], ele é executado automaticamente pelo hook após a gravação do `resultados.csv` (veja "O que é gerado")
- Requer a dependência abaixo instalada:

```bash
# Instalar dependências Python
pip install pandas scipy
```

## O que é gerado

| Arquivo | Descrição |
|---|---|
| `reports/relatorio_<Parceiro>.md` | Relatório detalhado por teste |
| `resultados.csv` | Consolidado de todos os testes analisados |

Os resultados são enviados automaticamente através do hook para o Google Sheets após a gravação do `resultados.csv`.

📊 **Planilha de resultados:** [Google Sheets](https://docs.google.com/spreadsheets/d/11n95hFQzc-ax-iLg6tuLK7R4-48DNH9zAth1S6dN7XI/edit?usp=sharing)

> **Verificação do upload:** cada envio ao Google Sheets é registrado em `scripts/upload_sheets.log`. Consulte esse arquivo para confirmar se o upload foi concluído com sucesso ou para diagnosticar eventuais falhas — ele guarda o histórico de cada tentativa de upload.

## Estrutura do projeto

```
├── .claude/
│   └── settings.json                # Hook (Stop) que envia o resultados.csv ao Google Sheets
├── CLAUDE.md                        # Instruções do agente
├── README.md
├── analyze.py                       # Script Python de análise
├── datasets/                        # CSVs dos testes A/B (entrada)
│   ├── dataset_01_parceiroA.csv
│   ├── dataset_02_parceiroB.csv
│   └── dataset_03_parceiroC.csv
├── DatasetsVisualizar/              # Versões .xlsx dos datasets para visualização (Não é gerado pela automação)
│   ├── dataset_01_parceiroAAlterado.xlsx
│   ├── dataset_02_parceiroBAlterado.xlsx
│   └── dataset_03_parceiroCAlterado.xlsx
├── reports/                         # Relatórios gerados pelo agente (um por parceiro)
│   ├── relatorio_<Parceiro>.md
│   └── Visualizar/
│       └── resultados.xlsx          # Versão .xlsx do consolidado apenas para visualização (Não é gerado pela automação)
├── resultados.csv                   # Planilha consolidada (saída)
├── link_planilha_google_sheets.txt  # Link da planilha no Google Sheets 
├── electric-block-*.json            # Credenciais da service account (Google Sheets API)
└── scripts/
    ├── upload_sheets.ps1            # Faz o upload do resultados.csv para o Google Sheets
    └── upload_sheets.log            # Log dos uploads ao Google Sheets
```
