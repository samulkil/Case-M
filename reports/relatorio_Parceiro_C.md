# Relatório de Teste A/B — Parceiro C

**Data da análise:** 2026-06-16
**Período do teste:** 01/07/2011 a 14/08/2011 (45 dias)
**Variantes testadas:** 2 (Grupo 1 e Grupo 2)

---

## Resumo executivo

O teste comparou duas variantes de cashback para o Parceiro C ao longo de 45 dias:

- **Grupo 1** — cashback de ~5,00% do GMV (Méliuz retém margem positiva de 2,00%)
- **Grupo 2** — cashback de ~7,00% do GMV (cashback = comissão, margem zero para o Méliuz)

Pela lógica de negócio, o **Grupo 1** é o vencedor provisório: é o único grupo com margem positiva e tem ROI de cashback bem superior (20,0x contra 14,3x).

**Porém, o teste estatístico é INCONCLUSIVO.** A diferença de vendas diárias médias entre os grupos não é estatisticamente significativa (t = 0,48, muito abaixo do limiar de 2,0 para 95% de confiança). Os volumes de vendas das duas variantes são estatisticamente equivalentes.

---

## Métricas por grupo

| Métrica | Grupo 1 | Grupo 2 |
|---|---|---|
| Compradores/dia | 101,1 | 100,5 |
| Ticket médio | R$ 382,16 | R$ 372,64 |
| Cashback rate | 5,00% | 7,00% |
| Margem Méliuz | 2,00% | 0,00% |
| ROI do cashback | 20,0x | 14,3x |
| Vendas totais | R$ 1.738.460 | R$ 1.685.235 |

Observações:
- **Volume:** praticamente empatado (101,1 vs 100,5 compradores/dia — diferença < 1%).
- **Eficiência:** Grupo 1 é mais eficiente (cashback rate 5,00% vs 7,00%).
- O Grupo 2 dobra o custo de cashback em relação à comissão e **não gera volume incremental** que o justifique: a margem do Méliuz cai a zero sem ganho de vendas.

---

## Análise estatística

Médias diárias de vendas (em milhares de R$) e desvio padrão:

| Grupo | n (dias) | Média diária | Desvio padrão |
|---|---|---|---|
| Grupo 1 | 45 | 38,63 | 9,99 |
| Grupo 2 | 45 | 37,45 | 13,31 |

**Teste t (par único, 2 grupos):**

- Erro padrão combinado = √(9,99²/45 + 13,31²/45) ≈ 2,48
- t = |38,63 − 37,45| / 2,48 = **0,48**

Como t = 0,48 < 2,0, a diferença **não é estatisticamente significativa** (não atinge 95% de confiança). As duas variantes produzem volumes de vendas estatisticamente indistinguíveis.

---

## Recomendação

**Resultado: INCONCLUSIVO — estender o teste.**

Não há evidência estatística de que o aumento de cashback (Grupo 2) gere volume incremental. As variantes empatam em volume, e escalar agora representa risco.

**Melhor grupo provisório: Grupo 1.** Caso fosse necessário decidir agora, escalaríamos o **Grupo 1** para 100% do tráfego: entrega o mesmo volume com cashback mais baixo (5,00% vs 7,00%), preservando margem positiva de 2,00% e ROI de 20,0x. O Grupo 2 apenas eleva o custo de cashback até zerar a margem, sem retorno em vendas.

Recomenda-se **estender o teste** para obter potência estatística suficiente antes de uma decisão definitiva.
