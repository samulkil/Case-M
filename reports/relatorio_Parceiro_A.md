# Relatório Teste A/B — Parceiro A

## Resumo Executivo

- **Período:** 01/01/2011 a 02/04/2011
- **Grupos testados:** Grupo 1, Grupo 2, Grupo 3
- **Decisão: Inconclusivo — estender teste (melhor grupo provisório: Grupo 1)**

## Métricas por Grupo

| Grupo | Compradores/dia | Ticket Médio | Cashback Rate | Margem Méliuz | ROI Cashback |
|-------|----------------|--------------|---------------|---------------|--------------|
| Grupo 1 | 104 | R$ 582 | 4.2% | 7.2% | 24.0x |
| Grupo 2 | 117 | R$ 594 | 5.8% | 5.6% | 17.3x |
| Grupo 3 | 124 | R$ 595 | 7.4% | 3.9% | 13.5x |

> **Cashback Rate**: quanto do GMV foi devolvido em cashback (menor = mais eficiente para o Méliuz)
> **Margem Méliuz**: (comissão - cashback) / vendas — quanto o Méliuz retém
> **ROI Cashback**: vendas geradas por cada R$ de cashback distribuído

## Análise Estatística

**Teste:** ANOVA omnibus + post-hoc Bonferroni.

**1. Omnibus (ANOVA):** F = 2.8733, p = 0.0582 → nenhuma diferença significativa entre os grupos (alpha = 0.05, 95% de confianca).

A ANOVA indica apenas SE existe diferença, nao entre QUAIS grupos. Como o omnibus NAO foi significativo, o post-hoc nao é interpretado (Fisher protegido).

**2. Post-hoc par a par (correção de Bonferroni):**

| Par | p bruto | p ajustado (Bonferroni) | Significativo? |
|---|---|---|---|
| Grupo 1 × Grupo 2 | 0.0863 | 0.2588 | Nao |
| Grupo 1 × Grupo 3 | 0.0196 | 0.0587 | Nao |
| Grupo 2 × Grupo 3 | 0.4996 | 1.0 | Nao |


## Recomendação

**Inconclusivo — recomenda-se estender o teste.**

Grupo 1 apresentou o melhor ROI de cashback (24.0x),
com margem de 7.2% para o Méliuz e cashback rate de
4.2% — o melhor equilíbrio entre volume de vendas e
custo de cashback entre os grupos testados.
Atenção: a diferença entre grupos não atingiu significância estatística — escalar agora representa risco. Recomenda-se coletar mais dados antes de decidir.
