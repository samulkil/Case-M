# Relatório de Teste A/B — Parceiro B

**Período analisado:** 01/05/2011 a 30/06/2011 (61 dias por grupo)
**Variantes testadas:** 3 grupos de cashback
**Data da análise:** 2026-06-16

## Resumo executivo

O teste comparou três níveis de cashback (% do GMV) para o Parceiro B. O **Grupo 1** (cashback rate de 4,00%) é o vencedor claro e estatisticamente significativo: entrega o **maior ROI do cashback (25,0x)**, a **maior margem Méliuz (7,00%)** e ainda o **maior volume** (131,0 compradores/dia). À medida que o cashback sobe (Grupo 2 com 6,00%, Grupo 3 com 8,89%), tanto a eficiência quanto a margem caem — sem ganho de volume.

**Recomendação: escalar o Grupo 1 para 100% do tráfego.**

## Métricas por grupo

| Grupo | Cashback Rate | Compradores/dia | Ticket Médio | Margem Méliuz | ROI Cashback |
|---|---|---|---|---|---|
| **Grupo 1** | **4,00%** | **131,0** | R$ 512,37 | **7,00%** | **25,0x** |
| Grupo 2 | 6,00% | 89,4 | R$ 525,13 | 5,00% | 16,7x |
| Grupo 3 | 8,89% | 81,4 | R$ 529,70 | 1,98% | 11,2x |

Totais Grupo 1: GMV R$ 4.093.818 · comissão R$ 450.321 · cashback R$ 163.751 · 7.990 compradores.
Totais Grupo 2: GMV R$ 2.863.019 · comissão R$ 314.935 · cashback R$ 171.778 · 5.452 compradores.
Totais Grupo 3: GMV R$ 2.629.963 · comissão R$ 285.725 · cashback R$ 233.780 · 4.965 compradores.

## Análise estatística (t-test / ANOVA, 95% de confiança)

Vendas diárias em milhares (R$ mil), fórmula computacional da variância (ddof=1); significância em t > 2,0.

| Grupo | Média diária (R$ mil) | Desvio padrão |
|---|---|---|
| Grupo 1 | 67,13 | 25,42 |
| Grupo 2 | 46,93 | 21,56 |
| Grupo 3 | 43,11 | 18,45 |

| Par | t-score | Significativo? |
|---|---|---|
| Grupo 1 × Grupo 2 | 4,73 | Sim |
| Grupo 1 × Grupo 3 | 5,97 | Sim |
| Grupo 2 × Grupo 3 | 1,05 | Não |

Com 3 grupos, aplica-se ANOVA: **a maioria dos pares (2 de 3) é significativa**, logo o resultado é **conclusivo**. As diferenças que importam — Grupo 1 contra os demais — são robustas. A diferença entre Grupo 2 e Grupo 3 entre si não é significativa, mas ambos são claramente inferiores ao Grupo 1.

## Trade-offs

- **Volume:** Grupo 1 lidera (131,0 compradores/dia vs 89,4 e 81,4). Aumentar o cashback não trouxe mais compradores — pelo contrário, os grupos com cashback maior atraíram menos usuários.
- **Eficiência:** Grupo 1 tem o menor cashback rate (4,00%) e maior ROI (25,0x). O Grupo 3 com 8,89% de cashback gera ROI de apenas 11,2x.
- **Alinhamento:** O vencedor por ROI é também o de maior volume e maior margem — não há trade-off a resolver. Os tickets médios são praticamente iguais entre grupos (R$ 512–530), confirmando que o cashback extra dos Grupos 2 e 3 não elevou o valor das compras, apenas comprimiu a margem.
- **Margem:** Grupo 3, com cashback de 8,89%, opera com margem de apenas 1,98% — perigosamente baixa e vulnerável a variações de comissão.

## Decisão

**Escalar o Grupo 1 (cashback 4,00% do GMV) para 100% do tráfego.** Maximiza simultaneamente ROI, margem e volume. Cashback adicional apenas corrói a margem sem retorno em volume ou ticket médio.
