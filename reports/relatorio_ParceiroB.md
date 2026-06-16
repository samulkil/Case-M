# Relatório de Teste A/B — Parceiro B

**Data da análise:** 2026-06-16
**Período do teste:** 2011-05-01 a 2011-06-30 (61 dias)
**Variantes testadas:** 3 grupos (cashback de 4,00% / 6,00% / 9,00% do GMV)

---

## Métricas por Grupo

| Métrica | Grupo 1 | Grupo 2 | Grupo 3 |
|---|---|---|---|
| Compradores totais | 7.990 | 5.452 | 5.029 |
| Compradores/dia | 131,0 | 89,4 | 82,4 |
| Vendas totais (GMV) | R$ 4.093.818 | R$ 2.863.019 | R$ 2.629.963 |
| Vendas/dia | R$ 67.112 | R$ 46.935 | R$ 43.114 |
| Comissão total | R$ 450.321 | R$ 314.935 | R$ 289.290 |
| Cashback total | R$ 163.751 | R$ 171.778 | R$ 236.697 |
| Ticket médio | R$ 512,37 | R$ 525,13 | R$ 522,96 |
| **Cashback rate** | **4,00%** | **6,00%** | **9,00%** |
| **Margem Méliuz** | **7,00%** | **5,00%** | **2,00%** |
| **ROI do cashback** | **25,0x** | **16,7x** | **11,1x** |

---

## Análise Estatística

Comparação das médias de vendas diárias entre pares (aproximação de t-test/ANOVA, 95% de confiança; significativo se `t > 2,0`):

| Par | Venda/dia (A) | Venda/dia (B) | t-score | Significativo (t>2)? |
|---|---|---|---|---|
| G1 vs G2 | R$ 67.112 | R$ 46.935 | 4,54 | ✅ Sim |
| G1 vs G3 | R$ 67.112 | R$ 43.114 | 5,70 | ✅ Sim |
| G2 vs G3 | R$ 46.935 | R$ 43.114 | 1,05 | ❌ Não |

**Resultado:** **2 de 3 pares** são estatisticamente significativos. Como a maioria dos pares atinge `t > 2,0`, o teste é **significativo** — o Grupo 1 difere de forma robusta dos demais.

---

## Determinação do Vencedor

1. Grupos com margem Méliuz positiva: todos os 3 grupos ✅
2. Maior ROI entre os grupos válidos: **Grupo 1 — ROI 25,0x**
3. Teste estatístico: **Significativo**

**Vencedor: Grupo 1 (cashback de 4,00% do GMV)**

---

## Trade-offs

| Dimensão | Análise |
|---|---|
| Eficiência | G1 tem menor cashback rate (4,00%), maior margem (7,00%) e maior ROI (25,0x) |
| Volume | G1 também lidera em compradores/dia (131,0 vs 89,4 do G2 e 82,4 do G3) |
| GMV | G1 gera o maior GMV/dia (R$ 67 mil), ~43% acima do G2 |

> **Destaque:** diferentemente de outros parceiros, aqui o Grupo 1 vence em **todas** as dimensões — eficiência, volume e GMV absoluto. Não há trade-off: o cashback menor atraiu mais compradores e mais vendas, com maior retorno.

---

## Recomendação

**Escalar Grupo 1 para 100% do tráfego.**

Cashback de 4,00% do GMV é a variante dominante: maior ROI (25,0x), maior margem Méliuz (7,00%), maior volume de compradores e maior GMV — com diferenças estatisticamente significativas em relação aos demais grupos. Decisão clara e sem trade-offs relevantes.
