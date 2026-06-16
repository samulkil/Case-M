# Relatório de Teste A/B — Parceiro A

**Data da análise:** 2026-06-16
**Período do teste:** 2011-01-01 a 2011-04-02 (92 dias)
**Variantes testadas:** 3 grupos (cashback de 4,16% / 5,77% / 7,42% do GMV)

---

## Métricas por Grupo

| Métrica | Grupo 1 | Grupo 2 | Grupo 3 |
|---|---|---|---|
| Compradores totais | 9.633 | 10.814 | 11.410 |
| Compradores/dia | 104,7 | 117,5 | 124,0 |
| Vendas totais (GMV) | R$ 5.605.173 | R$ 6.423.096 | R$ 6.785.856 |
| Vendas/dia | R$ 60.927 | R$ 69.816 | R$ 73.760 |
| Comissão total | R$ 638.135 | R$ 728.178 | R$ 767.887 |
| Cashback total | R$ 233.424 | R$ 370.659 | R$ 503.600 |
| Ticket médio | R$ 581,86 | R$ 593,96 | R$ 594,73 |
| **Cashback rate** | **4,16%** | **5,77%** | **7,42%** |
| **Margem Méliuz** | **7,22%** | **5,57%** | **3,89%** |
| **ROI do cashback** | **24,0x** | **17,3x** | **13,5x** |

---

## Análise Estatística

Comparação das médias de vendas diárias entre pares (aproximação de t-test/ANOVA, 95% de confiança; significativo se `t > 2,0`):

| Par | Venda/dia (A) | Venda/dia (B) | t-score | Significativo (t>2)? |
|---|---|---|---|---|
| G1 vs G2 | R$ 60.927 | R$ 69.816 | 1,72 | ❌ Não |
| G1 vs G3 | R$ 60.927 | R$ 73.760 | 2,35 | ✅ Sim |
| G2 vs G3 | R$ 69.816 | R$ 73.760 | 0,68 | ❌ Não |

Desvios-padrão das vendas diárias: G1 ≈ R$ 32,0 mil, G2 ≈ R$ 37,7 mil, G3 ≈ R$ 41,3 mil (alta variabilidade diária, com picos sazonais).

**Resultado:** apenas **1 de 3 pares** é estatisticamente significativo. Como a maioria dos pares **não** atinge `t > 2,0`, o teste é considerado **NÃO significativo**.

---

## Determinação do Vencedor

1. Grupos com margem Méliuz positiva: todos os 3 grupos ✅
2. Maior ROI entre os grupos válidos: **Grupo 1 — ROI 24,0x** (vencedor provisório)
3. Teste estatístico: **Não significativo** → resultado **Inconclusivo**

**Resultado: INCONCLUSIVO.** O Grupo 1 é o melhor candidato provisório, mas as diferenças de GMV diário entre os grupos não são estatisticamente robustas o suficiente para decisão definitiva.

---

## Trade-offs

| Dimensão | Análise |
|---|---|
| Eficiência | G1 tem menor cashback rate (4,16%) e maior margem (7,22%) e maior ROI (24,0x) |
| Volume | G3 atrai ~18% mais compradores/dia que G1 (124,0 vs 104,7) |
| GMV | G3 gera +21% de GMV/dia, mas à custa de cashback 116% maior por real de venda |

> **Atenção:** embora o Grupo 1 lidere em eficiência (ROI e margem), o maior volume/GMV vem do Grupo 3. O par G1 vs G2 não é estatisticamente significativo, então não há evidência conclusiva de que o cashback menor não prejudique o GMV.

---

## Recomendação

**Estender o teste antes de escalar.** A análise aponta o **Grupo 1 (cashback 4,16% do GMV)** como melhor candidato por eficiência (ROI 24,0x, margem 7,22%), mas a diferença de vendas diárias entre os grupos não alcança significância estatística na maioria dos pares (apenas G1 vs G3). Recomenda-se prolongar a coleta de dados para reduzir a incerteza antes de direcionar 100% do tráfego.
