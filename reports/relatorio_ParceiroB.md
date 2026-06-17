# Relatório de Teste A/B — Parceiro B

**Data da análise:** 2026-06-17
**Período:** 2011-05-01 a 2011-06-30 (61 dias por grupo)
**Dataset:** `dataset_02_parceiroB.csv`

## Recomendação

**Escalar o Grupo 1 (cashback 4,00% do GMV) para 100% do tráfego.**

O Grupo 1 combina a maior eficiência (menor cashback rate), a maior margem para o Méliuz, o maior ROI do cashback **e** o maior volume de compradores/dia. É vencedor em todas as dimensões relevantes, e a vantagem é estatisticamente robusta (95% de confiança) contra os dois outros grupos.

## Métricas por grupo

| Métrica | Grupo 1 (4,00%) | Grupo 2 (6,00%) | Grupo 3 (9,00%) |
|---|---|---|---|
| Compradores (total) | 7.990 | 5.452 | 5.029 |
| Comissão total | R$ 450.321 | R$ 314.935 | R$ 289.290 |
| Cashback total | R$ 163.751 | R$ 171.778 | R$ 236.697 |
| Vendas totais (GMV) | R$ 4.093.818 | R$ 2.863.019 | R$ 2.629.963 |
| Ticket médio | R$ 512,37 | R$ 525,13 | R$ 522,96 |
| **Cashback rate** | **4,00%** | 6,00% | 9,00% |
| **Margem Méliuz** | **7,00%** | 5,00% | 2,00% |
| **ROI do cashback** | **25,0x** | 16,7x | 11,1x |
| Compradores/dia | **131,0** | 89,4 | 82,4 |

O cashback mais generoso (G2, G3) **não** gerou ticket médio maior nem mais volume — pelo contrário, o G1, com o menor cashback, foi quem trouxe mais compradores e maior GMV. Cada real de cashback no G1 retorna R$ 25,00 em vendas, contra R$ 11,10 no G3.

## Análise estatística (95% de confiança)

Variável testada: vendas diárias (GMV), em milhares de R$. Com 3 grupos, o fluxo tem duas etapas.

### Etapa 1 — ANOVA omnibus (teste F)

Verifica SE existe alguma diferença entre os grupos.

| | Valor |
|---|---|
| SQ entre grupos | 20.284,44 |
| SQ dentro dos grupos | 92.788,34 |
| gl entre | 2 |
| gl dentro | 180 |
| **F** | **19,68** |
| F crítico (gl_entre=2, α=0,05) | 3,0 |

**Veredito:** F = 19,68 > 3,0 → **omnibus SIGNIFICATIVO**. Existe pelo menos um par de grupos com vendas diárias médias diferentes. Prossegue-se ao post-hoc.

### Etapa 2 — Post-hoc par a par (Bonferroni)

Identifica ENTRE QUAIS grupos está a diferença. Com m = 3 pares, o limiar de Bonferroni é t crítico = 2,4.

| Par | t-score | Limiar Bonferroni | Significativo? |
|---|---|---|---|
| Grupo 1 vs Grupo 2 | 4,54 | 2,4 | **Sim** |
| Grupo 1 vs Grupo 3 | 5,70 | 2,4 | **Sim** |
| Grupo 2 vs Grupo 3 | 1,05 | 2,4 | Não |

**Leitura:** o Grupo 1 difere de forma estatisticamente robusta tanto do Grupo 2 quanto do Grupo 3. Grupo 2 e Grupo 3 não diferem entre si. A superioridade de volume/GMV do Grupo 1 é, portanto, conclusiva.

(Médias diárias de vendas, em milhares: G1 = 67,1; G2 = 46,9; G3 = 43,1.)

## Trade-offs

- **Volume:** Grupo 1 lidera (131,0 compradores/dia vs 89,4 e 82,4).
- **Eficiência:** Grupo 1 lidera (cashback rate 4,00%, o menor).
- Não há trade-off a ponderar: o vencedor por ROI **é também** o de maior volume. Não há tensão entre eficiência e escala neste teste.

## Decisão final

**Escalar o Grupo 1 (4,00% de cashback) para 100% do tráfego.** ROI de 25,0x e margem Méliuz de 7,00%, com cashback rate mais eficiente e maior volume. Vantagem estatisticamente significativa contra G2 e G3 (95% de confiança).
