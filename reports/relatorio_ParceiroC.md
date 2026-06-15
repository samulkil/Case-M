# Relatório de Análise — Teste A/B Parceiro C

**Data da análise:** 2026-06-15  
**Período do teste:** 2011-07-01 a 2011-08-14 (45 dias)  
**Grupos:** Grupo 1 (5% cashback) · Grupo 2 (7% cashback — igual à comissão)

---

## Métricas por Grupo

| Métrica | Grupo 1 | Grupo 2 |
|---|---|---|
| Vendas totais | R$ 1.738.460 | R$ 1.685.235 |
| Cashback distribuído | R$ 86.923 | R$ 117.966 |
| Comissão recebida¹ | R$ 121.692 | R$ 117.966 |
| **Cashback rate** | **5,0%** | **7,0%** |
| **Margem Méliuz** | **2,0%** | **0,0%** |
| **ROI do cashback** | **20,0x** | **14,3x** |
| Compradores totais | 4.549 | 4.522 |
| **Compradores/dia** | **101,1** | **100,5** |
| Ticket médio | R$ 382 | R$ 373 |

¹ Taxa de comissão constante de 7% sobre vendas (este parceiro paga comissão menor que os demais), verificada em todas as linhas do dataset.

---

## Análise Comparativa

### Alerta crítico: Grupo 2 tem margem zero
No Grupo 2, o cashback distribuído é **idêntico** ao valor de comissão recebida em todas as datas do teste. Isso significa que o Méliuz não retém nenhuma margem neste grupo — cada real de comissão é integralmente repassado ao usuário.

### Volume de compradores
Os dois grupos têm volume praticamente idêntico (101,1 vs 100,5 compradores/dia, diferença de **0,6%** — irrelevante). O cashback maior não trouxe nenhum benefício em aquisição de compradores.

### Comissão do parceiro
A taxa de comissão deste parceiro é de 7% (vs 11% dos Parceiros A e B), o que deixa margem operacional muito estreita mesmo no melhor cenário.

---

## Recomendação

### ✅ Escalar Grupo 1 para 100% do tráfego

O Grupo 2 é inviável: margem zero significa que qualquer custo operacional adicional (fraude, suporte, chargeback) já torna o parceiro deficitário. O Grupo 1 com 2% de margem é financeiramente superior e atrai praticamente a mesma quantidade de compradores (diferença de 0,6%).

**Observação estratégica:** A margem de 2% do G1 ainda é baixa em comparação com outros parceiros. Vale renegociar a taxa de comissão com o Parceiro C antes de escalar, ou avaliar se este parceiro é prioritário no portfólio.
