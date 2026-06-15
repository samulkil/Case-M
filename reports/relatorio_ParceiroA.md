# Relatório de Análise — Teste A/B Parceiro A

**Data da análise:** 2026-06-15  
**Período do teste:** 2011-01-01 a 2011-04-02 (92 dias)  
**Grupos:** Grupo 1 (menor cashback) · Grupo 2 (cashback médio) · Grupo 3 (maior cashback)

---

## Métricas por Grupo

| Métrica | Grupo 1 | Grupo 2 | Grupo 3 |
|---|---|---|---|
| Vendas totais | R$ 5.605.173 | R$ 6.423.096 | R$ 6.785.856 |
| Cashback distribuído | R$ 233.424 | R$ 370.659 | R$ 503.600 |
| Comissão recebida¹ | R$ 616.569 | R$ 706.540 | R$ 746.444 |
| **Cashback rate** | **4,16%** | **5,77%** | **7,42%** |
| **Margem Méliuz** | **6,84%** | **5,23%** | **3,58%** |
| **ROI do cashback** | **24,0x** | **17,3x** | **13,5x** |
| Compradores totais | 9.633 | 10.814 | 11.410 |
| **Compradores/dia** | **104,7** | **117,5** | **124,0** |
| Ticket médio | R$ 581,90 | R$ 593,80 | R$ 594,70 |

¹ Taxa de comissão constante de 11% sobre vendas, verificada em todas as linhas do dataset.

---

## Análise Comparativa

### ROI e Margem
O Grupo 1 lidera com folga em eficiência financeira:
- ROI 39% superior ao G2 e 78% superior ao G3
- Margem Méliuz 1,61 p.p. acima do G2 e 3,26 p.p. acima do G3

### Volume de compradores
O G3 atrai mais compradores (124/dia vs 104,7 do G1), diferença de +18%. O G2 fica no meio (+12% sobre G1). Os tickets médios são praticamente idênticos entre os 3 grupos (~R$ 582–595).

### Trade-off central
Mais cashback atrai mais compradores, mas o custo cresce desproporcionalmente. O G3 gera +19 compradores/dia em relação ao G1, mas o cashback rate é quase o dobro (7,42% vs 4,16%). A diferença de margem entre G1 e G3 é de 3,26 p.p. — bem acima do limiar de 5% considerado significativo para decisão.

Estimativa: ao escalar G3 em vez do G1, o Méliuz gastaria ~**R$ 270.000 a mais em cashback por ano** sem retorno proporcional em vendas.

---

## Recomendação

### ✅ Escalar Grupo 1 para 100% do tráfego

O Grupo 1 oferece o melhor ROI (24x), a maior margem (6,84%) e tickets similares aos demais grupos. A perda de ~19 compradores/dia em relação ao G3 não justifica o custo adicional de cashback. O G2 poderia ser considerado se a prioridade estratégica for crescimento de base, mas o G1 é a escolha financeiramente mais saudável.
