# Relatório de Teste A/B — Parceiro A

**Dataset:** `dataset_01_parceiroA.csv`
**Período do teste:** 2011-01-01 a 2011-04-02 (92 dias por grupo)
**Variantes testadas:** 3 grupos (cashback de 4,16% / 5,77% / 7,42% do GMV)
**Data da análise:** 2026-06-17

---

## Resumo executivo

O teste comparou três níveis de cashback. Por critério de negócio, o **Grupo 1** (cashback mais baixo, 4,16% do GMV) é o vencedor provisório: maior ROI do cashback (24,0x) e maior margem Méliuz (7,22%). **Contudo, o teste estatístico não confirma a diferença com 95% de confiança** — a ANOVA omnibus ficou abaixo do limiar crítico (F = 2,87 ≤ 3,0).

**Recomendação: Inconclusivo. Estender o teste antes de escalar.** Melhor grupo provisório: Grupo 1.

---

## Métricas por grupo

| Métrica | Grupo 1 | Grupo 2 | Grupo 3 |
|---|---|---|---|
| Compradores totais | 9.633 | 10.814 | 11.410 |
| Compradores/dia | 104,7 | 117,5 | 124,0 |
| Vendas totais (GMV) | R$ 5.605.173 | R$ 6.423.096 | R$ 6.785.856 |
| Comissão total | R$ 638.135 | R$ 728.178 | R$ 767.887 |
| Cashback total | R$ 233.424 | R$ 370.659 | R$ 503.600 |
| Dias | 92 | 92 | 92 |
| Ticket médio | R$ 581,85 | R$ 593,96 | R$ 594,73 |
| **Cashback rate** | **4,16%** | **5,77%** | **7,42%** |
| **Margem Méliuz** | **7,22%** | **5,57%** | **3,89%** |
| **ROI do cashback** | **24,0x** | **17,3x** | **13,5x** |

---

## Determinação do vencedor (critério de negócio)

1. Grupos com margem Méliuz positiva: **todos os 3** são válidos.
2. Entre os válidos, o de **maior ROI do cashback** é o **Grupo 1 (24,0x)** → vencedor provisório.

À medida que o cashback sobe (G1 → G2 → G3), o volume cresce, mas a eficiência cai fortemente: o ROI vai de 24,0x para 13,5x e a margem de 7,22% para 3,89%. O cashback adicional não se paga em volume.

---

## Análise estatística (95% de confiança)

Com **3 grupos**, o fluxo correto tem **duas etapas**: (1) **ANOVA omnibus** (teste F — existe diferença entre algum par?) e, **somente se ela for significativa**, (2) **post-hoc par a par com correção de Bonferroni** (entre quais grupos está a diferença).

Estatísticas das vendas diárias (em milhares de R$), n = 92 por grupo:

| Grupo | Média diária | Desvio padrão |
|---|---|---|
| Grupo 1 | 60,93 | 32,02 |
| Grupo 2 | 69,82 | 37,67 |
| Grupo 3 | 73,76 | 41,31 |

### Etapa 1 — ANOVA omnibus (teste F)

- SQ entre grupos = 7.952,17 — gl = 2
- SQ dentro dos grupos = 377.744,57 — gl = 273
- **F = (7.952,17 / 2) / (377.744,57 / 273) = 3.976,09 / 1.383,68 = 2,87**
- F crítico (gl entre = 2; α = 0,05) ≈ **3,0**

**Veredito: F = 2,87 ≤ 3,0 → omnibus NÃO significativo.** Não há evidência, a 95% de confiança, de que algum par de grupos difira em vendas diárias.

### Etapa 2 — Post-hoc Bonferroni

**Não aplicável.** Como o omnibus não foi significativo, pela regra do teste protegido (Fisher) o post-hoc não deve ser executado nem interpretado. As comparações par a par só seriam válidas se a ANOVA tivesse rejeitado a hipótese nula.

---

## Trade-offs

| Dimensão | Análise |
|---|---|
| Eficiência | **Grupo 1** — menor cashback rate (4,16%), maior margem (7,22%) e maior ROI (24,0x) |
| Volume | **Grupo 3** — maior tráfego (124,0 compradores/dia, +18% vs G1) |
| GMV | G3 gera mais GMV/dia, mas à custa de cashback muito maior por real vendido |

> **Atenção:** o vencedor provisório por ROI (Grupo 1) **não é o de maior volume** (Grupo 3). Subir o cashback atrai mais compradores, mas corrói margem e ROI.

---

## Recomendação

**Inconclusivo — não escalar ainda. Estender o teste.**

O Grupo 1 (cashback 4,16% do GMV) lidera em eficiência (ROI 24,0x, margem 7,22%), mas a diferença de desempenho entre os grupos não é estatisticamente robusta a 95% de confiança (ANOVA F = 2,87, abaixo do crítico 3,0). Recomenda-se prolongar a coleta de dados antes de direcionar 100% do tráfego. Caso uma aposta provisória seja necessária, o **Grupo 1** é o candidato mais eficiente.
