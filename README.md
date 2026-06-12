# Analisador de Testes A/B — Méliuz

Solução reutilizável para análise de testes A/B de cashback. Basta abrir o Claude Code na pasta do projeto e fazer a pergunta em linguagem natural — sem instalações, sem dependências.

## Como usar

1. Clone o repositório
2. Abra o **Claude Code desktop** na pasta do projeto
3. Digite a pergunta:
   > "Dado esse teste A/B, qual variante de cashback devemos escalar pra 100% do tráfego?"
4. O Claude vai listar os datasets disponíveis em `datasets/` e perguntar quais analisar
5. Escolha os datasets e receba a análise completa

## O que é gerado

- `reports/relatorio_<Parceiro>.md` — relatório detalhado por teste, apresentável para um gestor
- `resultados.csv` — planilha consolidada com todos os testes analisados

## Estrutura do projeto

```
├── CLAUDE.md              # Instruções do agente
├── README.md
├── datasets/              # CSVs dos testes A/B
│   ├── dataset_01_parceiroA.csv
│   ├── dataset_02_parceiroB.csv
│   └── dataset_03_parceiroC.csv
├── reports/               # Relatórios gerados
├── resultados.csv         # Planilha consolidada
└── analyze.py             # Alternativa: rodar via Python (opcional)
```

## Alternativa via Python (opcional)

Se preferir rodar sem o Claude Code:

```bash
pip install pandas scipy
python analyze.py datasets/dataset_01_parceiroA.csv
```
