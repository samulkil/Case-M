# Relatório de Teste A/B — Parceiro C

**Data da análise:** 2026-06-17
**Dataset:** `dataset_03_parceiroC.csv`
**Período:** 2011-07-01 a 2011-08-14 (45 dias por grupo)
**Variantes:** 2 grupos

---

## 1. Resumo executivo

O teste comparou duas configurações de cashback do Parceiro C. O **Grupo 1** (cashback rate de 5,00% do GMV) é o **vencedor provisório por critério de negócio**: é o único grupo com **margem Méliuz positiva** (2,00%) e tem o **maior ROI do cashback** (20,0x). O Grupo 2 distribui mais cashback (7,00% do GMV) com margem zero — repassa toda a comissão como cashback, não sobrando margem para o Méliuz.

**Porém, o teste estatístico NÃO é conclusivo:** a diferença de volume de vendas diárias entre os grupos não é estatisticamente significativa (t = 0,48, muito abaixo do limiar de 2,0). A vantagem do Grupo 1 é clara em eficiência econômica (margem e ROI), mas a diferença de GMV gerado entre os grupos pode ser ruído.

---

## 2. Métricas por grupo

| Métrica | Grupo 1 | Grupo 2 |
|---|---|---|
| Compradores (total) | 4.549 | 4.522 |
| Comissão total | R$ 121.693 | R$ 117.967 |
| Cashback total | R$ 86.924 | R$ 117.967 |
| Vendas totais (GMV) | R$ 1.738.460 | R$ 1.685.235 |
| Dias | 45 | 45 |
| **Ticket médio** | **R$ 382,16** | **R$ 372,67** |
| **Cashback rate** | **5,00%** | **7,00%** |
| **Margem Méliuz** | **2,00%** | **0,00%** |
| **ROI do cashback** | **20,0x** | **14,3x** |
| **Compradores/dia** | **101,1** | **100,5** |

---

## 3. Determinação do vencedor

1. **Filtro de margem positiva:** apenas o **Grupo 1** tem margem Méliuz > 0 (2,00%). O Grupo 2 tem margem 0,00% (toda a comissão é devolvida como cashback).
2. Entre os grupos válidos (apenas Grupo 1), ele também tem o maior ROI do cashback (20,0x vs 14,3x).
3. **Vencedor provisório por negócio: Grupo 1.**

---

## 4. Análise estatística (95% de confiança)

Com **2 grupos**, aplica-se um **teste t único** sobre as vendas diárias (em milhares), sem correção para múltiplas comparações (há uma única comparação). Não se aplica ANOVA omnibus nem post-hoc Bonferroni — esses são reservados para 3+ grupos.

| Grupo | Média diária (R$ mil) | Desvio padrão (R$ mil) | n (dias) |
|---|---|---|---|
| Grupo 1 | 38,63 | 9,99 | 45 |
| Grupo 2 | 37,45 | 13,31 | 45 |

- Erro padrão combinado = √(9,99²/45 + 13,31²/45) = 2,481
- **t = |38,63 − 37,45| / 2,481 = 0,48**
- Limiar de significância: **t > 2,0**
- **Veredito: t = 0,48 ≤ 2,0 → diferença NÃO significativa.**

A diferença no GMV diário entre os grupos não é estatisticamente distinguível de ruído ao nível de 95%.

---

## 5. Trade-offs

- **Volume (compradores/dia):** praticamente empatados — Grupo 1 com 101,1 e Grupo 2 com 100,5. O vencedor por ROI (Grupo 1) também é o de maior volume, então não há conflito volume vs. eficiência aqui.
- **Eficiência (cashback rate):** Grupo 1 é mais eficiente (5,00% vs 7,00%) — entrega volume equivalente gastando menos cashback.
- **Margem:** Grupo 1 preserva 2,00% de margem; Grupo 2 zera a margem ao repassar toda a comissão como cashback.

---

## 6. Recomendação

**Provisoriamente, escalar o Grupo 1** (cashback de 5,00%): mesma tração de volume com cashback mais barato, preservando margem positiva e ROI superior. O Grupo 2, com cashback de 7,00%, não traz volume adicional que justifique zerar a margem.

**Ressalva estatística:** a diferença de GMV diário entre os grupos é inconclusiva (t = 0,48). A decisão pelo Grupo 1 se sustenta no critério econômico (margem e ROI), não em diferença estatística de desempenho de vendas. Caso a prioridade seja certeza estatística sobre o impacto em GMV, recomenda-se estender o teste para acumular mais dados.
