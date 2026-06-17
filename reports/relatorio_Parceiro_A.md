# Relatório de Teste A/B — Parceiro A

**Data da análise:** 2026-06-16
**Período do teste:** 01/01/2011 a 02/04/2011 (92 dias)
**Variantes testadas:** 3 grupos de cashback

---

## Resumo executivo

O teste comparou três níveis de cashback do Parceiro A ao longo de 92 dias.
À medida que o cashback aumenta (G1 → G2 → G3), o **volume** de compradores
cresce, mas a **eficiência** (margem Méliuz e ROI do cashback) cai.

O **Grupo 1** é o melhor em rentabilidade: maior ROI do cashback (24,0x),
maior margem Méliuz (7,22%) e menor cashback rate (4,16%). Porém, o
**teste estatístico é inconclusivo** — apenas 1 de 3 pares atinge
significância (t > 2,0). Recomenda-se **estender o teste** antes de escalar.

---

## Métricas por grupo

| Grupo | Compradores/dia | Ticket Médio | Cashback Rate | Margem Méliuz | ROI Cashback |
|---|---|---|---|---|---|
| Grupo 1 | 104,7 | R$ 581,87 | 4,16% | 7,22% | 24,0x |
| Grupo 2 | 117,5 | R$ 593,96 | 5,77% | 5,57% | 17,3x |
| Grupo 3 | 124,0 | R$ 594,73 | 7,42% | 3,89% | 13,5x |

Totais do período (92 dias cada grupo):

| Grupo | Compradores | Comissão | Cashback | Vendas (GMV) |
|---|---|---|---|---|
| Grupo 1 | 9.633 | R$ 638.135,00 | R$ 233.424,00 | R$ 5.605.173,00 |
| Grupo 2 | 10.814 | R$ 728.178,00 | R$ 370.659,00 | R$ 6.423.096,00 |
| Grupo 3 | 11.410 | R$ 767.887,00 | R$ 503.600,00 | R$ 6.785.856,00 |

---

## Análise estatística (aproximação t-test / ANOVA, 95%)

Vendas diárias em milhares de R$. Médias e desvios-padrão diários:

| Grupo | n (dias) | Média diária | Desvio-padrão |
|---|---|---|---|
| Grupo 1 | 92 | 60,93 | 32,02 |
| Grupo 2 | 92 | 69,82 | 37,67 |
| Grupo 3 | 92 | 73,76 | 41,31 |

T-scores por par:

| Par | t-score | Significativo (t > 2,0)? |
|---|---|---|
| G1 x G2 | 1,72 | Não |
| G1 x G3 | 2,36 | Sim |
| G2 x G3 | 0,68 | Não |

Com 3 grupos, aplica-se o critério ANOVA (maioria dos pares). Apenas
**1 de 3 pares** é significativo — não há maioria. **Resultado: inconclusivo.**

---

## Trade-offs

- **Volume:** Grupo 3 lidera (124,0 compradores/dia) — maior cashback atrai mais compradores.
- **Eficiência:** Grupo 1 é o mais eficiente (cashback rate 4,16%, ROI 24,0x).
- O vencedor provisório por ROI (Grupo 1) **não** é o de maior volume (Grupo 3) — há tensão clara entre crescimento e rentabilidade.

---

## Recomendação

**Qual variante escalar para 100% do tráfego?**

No momento, **nenhuma com confiança estatística**. As diferenças de vendas
diárias entre grupos não são consistentemente significativas (apenas G1xG3).
Recomenda-se **estender o teste** para acumular mais dias e reduzir a
variância antes de decidir.

Se uma decisão for forçada hoje, o **Grupo 1** é o melhor candidato
provisório, por maximizar margem e ROI do cashback com a menor distribuição
de cashback.
