# Relatório de Teste A/B — Parceiro C

**Data da análise:** 2026-06-16
**Período do teste:** 2011-07-01 a 2011-08-14 (45 dias)
**Variantes testadas:** 2 grupos (cashback de 5,00% / 7,00% do GMV)

---

## Métricas por Grupo

| Métrica | Grupo 1 | Grupo 2 |
|---|---|---|
| Compradores totais | 4.549 | 4.522 |
| Compradores/dia | 101,1 | 100,5 |
| Vendas totais (GMV) | R$ 1.738.460 | R$ 1.685.235 |
| Vendas/dia | R$ 38.632 | R$ 37.450 |
| Comissão total | R$ 121.693 | R$ 117.967 |
| Cashback total | R$ 86.924 | R$ 117.967 |
| Ticket médio | R$ 382,16 | R$ 372,68 |
| **Cashback rate** | **5,00%** | **7,00%** |
| **Margem Méliuz** | **2,00%** | **0,00%** |
| **ROI do cashback** | **20,0x** | **14,3x** |

> ⚠️ **Observação:** No Grupo 2, a comissão recebida do parceiro é integralmente repassada como cashback (comissão = cashback em todos os dias). O Méliuz não obtém margem nesta variante.

---

## Análise Estatística

Comparação das médias de vendas diárias entre os 2 grupos (aproximação de t-test, 95% de confiança; significativo se `t > 2,0`):

| Par | Venda/dia (A) | Venda/dia (B) | t-score | Significativo (t>2)? |
|---|---|---|---|---|
| G1 vs G2 | R$ 38.632 | R$ 37.450 | 0,48 | ❌ Não |

**Resultado:** `t = 0,48` está bem abaixo do limiar de 2,0. A diferença de GMV diário (apenas 3,2%) **não é estatisticamente significativa**.

---

## Determinação do Vencedor

1. Grupos com margem Méliuz positiva: apenas **Grupo 1** (2,00%) — G2 tem margem zero e é descartado
2. Grupo válido único: Grupo 1 (ROI 20,0x) — vencedor provisório
3. Teste estatístico: **Não significativo** (`t = 0,48`)

**Resultado: INCONCLUSIVO — recomenda-se estender o teste.**
Melhor grupo provisório: **Grupo 1**

---

## Trade-offs

| Dimensão | Análise |
|---|---|
| Margem | Apenas G1 é lucrativo (2,00%); G2 tem margem zero — sem viabilidade de escala |
| Volume | Grupos praticamente idênticos (101,1 vs 100,5 compradores/dia) |
| GMV | Diferença de apenas 3,2% no GMV/dia — não distinguível estatisticamente |
| ROI | G1: 20,0x vs G2: 14,3x — G1 superior, mas a diferença de GMV não é significativa |

> **Ponto crítico:** Embora G2 não tenha margem, as diferenças de comportamento (GMV, compradores) são mínimas. O cashback maior não está gerando tração adicional no curto período testado.

---

## Recomendação

**Inconclusivo — estender o teste por mais tempo.**

A diferença de GMV entre os grupos é de apenas 3,2% (`t = 0,48`), abaixo do limiar de significância. G1 é o único grupo com margem positiva (2,00%) e o grupo provisoriamente preferível. Recomenda-se ampliar o período de teste para confirmar se há diferença real de comportamento de compra.

Caso seja necessária uma decisão imediata, **escalar G1** (5,00% de cashback) é a escolha conservadora — garante margem positiva e ROI superior.
