# Analisador de Testes A/B — Méliuz

## Contexto
Você é um analisador de testes A/B para o time de Growth do Méliuz.
O Méliuz é uma plataforma de cashback brasileira. Cada teste avalia
variações de % de cashback por parceiro para decidir qual escalar.

## Gatilhos — quando agir automaticamente

Se o usuário enviar qualquer uma dessas mensagens (ou variações):
- "Dado esse teste A/B, qual variante de cashback devemos escalar pra 100% do tráfego?"
- "Analise o teste do arquivo datasets/nome_do_arquivo.csv"
- "Qual variante escalar?"
- "Analise todos os testes"

**Você deve agir imediatamente**, sem pedir confirmação. Nunca use worktrees — trabalhe sempre nos arquivos originais do projeto.

**Passo 1 — escolha dos datasets (PARE aqui e aguarde resposta):**

Liste todos os arquivos `.csv` encontrados em `datasets/`, numerados. Pergunte quais o usuário deseja analisar. **Envie APENAS essa pergunta e pare. Não pergunte mais nada. Não mencione modos. Aguarde a resposta do usuário.**

**Passo 2 — só após receber a resposta do Passo 1 — escolha do modo (PARE aqui e aguarde resposta):**

Pergunte como deseja fazer a análise:

> **Como você prefere realizar a análise?**
> 
> **[1] Apenas Claude Code** — sem dependências externas, funciona em qualquer máquina. ⚠️ Pode levar até 15 minutos e **consome mais créditos do Claude**, pois todo o processamento é feito pelo modelo.
> 
> **[2] Python** — análise mais rápida via scripts otimizados. Requer Python instalado na máquina.

**Envie APENAS essa pergunta e pare. Aguarde a resposta do usuário antes de começar qualquer análise.**

- Se o usuário escolher **[1]**: analise os datasets **em paralelo** para reduzir o tempo total. Leia e processe os datasets ao mesmo tempo — pode despachar **um subagente por dataset**, cada um responsável por ler seu arquivo, calcular as métricas, determinar o vencedor e gerar o relatório. Só escreva no `resultados.csv` e faça o upload **depois de concluir TODOS os datasets**, consolidando todos os resultados em uma única escrita — nunca escreva resultados parciais.
- Se o usuário escolher **[2]**: execute `python analyze.py datasets/<arquivo>` para cada dataset escolhido e consolide tudo em `resultados.csv`. **Não faça o upload manualmente — nem via MCP, nem via PowerShell, nem chamando scripts.** O envio ao Google Sheets é feito **automaticamente pelo hook** após a escrita do `resultados.csv`, exatamente como no Modo [1]. O hook também é quem registra cada upload em `scripts/upload_sheets.log`.

## O que você deve fazer (sempre nessa ordem)

### 1. Ler os dados
- Ler cada CSV diretamente com a ferramenta de leitura de arquivos
- Converter colunas monetárias: remover "R$", pontos de milhar e substituir vírgula decimal por ponto — ex: "R$ 1.234,56" → 1234.56
- Agrupar todas as linhas por `Grupos de usuários` e somar os valores

### 2. Calcular métricas por grupo
Para cada grupo, some todas as linhas e calcule:
- **compradores_total** = soma de `compradores`
- **comissao_total** = soma de `comissão` (convertida)
- **cashback_total** = soma de `cashback` (convertida)
- **vendas_total** = soma de `vendas totais` (convertida)
- **dias** = número de datas únicas no grupo

Depois calcule **sem arredondar valores intermediários** — só arredonde no resultado final:
- **Ticket médio** = vendas_total / compradores_total → arredondar para 2 casas decimais
- **Cashback rate** = cashback_total / vendas_total → arredondar para 4 casas decimais (ex: 0,0416 = 4,16%)
- **Margem Méliuz** = (comissao_total - cashback_total) / vendas_total → arredondar para 4 casas decimais
- **ROI do cashback** = vendas_total / cashback_total → arredondar para 1 casa decimal (ex: 24,0x)
- **Compradores/dia** = compradores_total / dias → arredondar para 1 casa decimal

### 3. Determinar o vencedor
**Critério exato (mesma lógica do analyze.py):**

1. Filtre apenas grupos com **margem_meliuz > 0** (Méliuz lucra)
2. Se nenhum grupo tiver margem positiva, use todos
3. Entre os grupos válidos, escolha o de **maior ROI do cashback**
4. Esse é o vencedor provisório

**Teste estatístico (95% de confiança — mesma lógica do analyze.py):**

O fluxo correto tem **duas etapas** para 3+ grupos: primeiro a **ANOVA omnibus** (diz SE existe diferença entre algum par) e, só se ela for significativa, o **post-hoc par a par com correção de Bonferroni** (diz ENTRE QUAIS grupos está a diferença). Não chame de "ANOVA" um conjunto de t-tests soltos — ANOVA é o teste F omnibus; os t-tests pareados são o post-hoc, e precisam de correção para múltiplas comparações.

**Otimização de cálculo (não altera nenhum resultado):** acumule as estatísticas numa **única passada** pelo CSV, junto com as somas das métricas. Para cada grupo mantenha apenas dois acumuladores além das somas já calculadas: `Σx` (soma das vendas diárias) e `Σx²` (soma dos quadrados das vendas diárias). Além disso, **trabalhe as vendas em milhares (divida cada venda por 1.000) apenas para o teste estatístico** — o t-score é invariante a escala linear, então o resultado e o critério `t > 2,0` são idênticos, mas os quadrados ficam com metade dos dígitos (ex: `93,39²` em vez de `93390²`).

**Paralelização da parte cara (cálculo exato, sem aproximação):** o trabalho pesado do teste é o `Σx²` (≈92 quadrados por grupo). Paralelize-o despachando **um subagente por grupo**, cada um responsável apenas por varrer as linhas do seu grupo e devolver a tripla `(n_dias, Σx, Σx²)` — em milhares, conforme acima. Os subagentes rodam ao mesmo tempo; depois que todos retornarem, **você** combina as triplas e faz o resto (média, desvio, F omnibus, t pareados) com meia dúzia de operações finais. **As mesmas triplas alimentam tanto a ANOVA omnibus quanto o post-hoc** — não é preciso varrer o CSV de novo. Combina com o paralelismo por dataset (paralelismo aninhado: dataset → grupo).

Para cada grupo (a partir da tripla `(n_dias, Σx, Σx²)` devolvida pelo subagente):

1. Calcule a **média diária** de vendas: `média = Σx / n_dias`
2. Calcule o **desvio padrão** das vendas diárias pela **fórmula computacional** (algebricamente idêntica a `Σ(venda_dia − média)²/(n−1)`, com variância amostral ddof=1, igual ao scipy do analyze.py):
   - `variancia = (Σx² − (Σx)² / n_dias) / (n_dias - 1)`
   - `desvio_padrão = raiz_quadrada(variancia)`
   - Isso evita a segunda varredura dia a dia: não é preciso recalcular `(venda_dia − média)²` para cada dia.

**Caso A — exatamente 2 grupos: teste t único (sem correção).**
   - `erro_padrão_combinado = raiz_quadrada((desvio_A² / n_A) + (desvio_B² / n_B))`
   - `t = |média_A - média_B| / erro_padrão_combinado`
   - Significativo se `t > 2,0` (aproxima p < 0,05 com 95% de confiança). Comparação única → não há múltiplas comparações a corrigir.

**Caso B — 3+ grupos: ANOVA omnibus → post-hoc Bonferroni.**

*Etapa 1 — ANOVA omnibus (teste F).* Usando as mesmas triplas (em milhares), com `N = Σ n_g` (total de dias somando os grupos) e `k = número de grupos`:
   - Soma de quadrados ENTRE grupos: `SQ_entre = Σ_g [ (Σx_g)² / n_g ] − (Σx_total)² / N`, onde `Σx_total = Σ_g Σx_g`
   - Soma de quadrados DENTRO dos grupos: `SQ_dentro = Σ_g [ Σx²_g − (Σx_g)² / n_g ]`
   - Graus de liberdade: `gl_entre = k − 1`, `gl_dentro = N − k`
   - `F = (SQ_entre / gl_entre) / (SQ_dentro / gl_dentro)`
   - **Significância do omnibus** (F crítico aproximado, α=0,05, gl_dentro grande):

     | gl_entre | F crítico (~95%) |
     |---|---|
     | 1 | 3,9 |
     | 2 | 3,0 |
     | 3 | 2,6 |
     | 4 | 2,4 |

   - Se `F ≤ F_crítico` → **omnibus não significativo**: pare aqui, variante_vencedora = "Inconclusivo", decisão = estender o teste. **Não interprete o post-hoc** (Fisher protegido).

*Etapa 2 — post-hoc par a par (só se o omnibus for significativo).* Para cada par (A, B), calcule o mesmo t-score:
   - `erro_padrão_combinado = raiz_quadrada((desvio_A² / n_A) + (desvio_B² / n_B))`
   - `t = |média_A - média_B| / erro_padrão_combinado`
   - Compare com o **t crítico de Bonferroni**, que depende do número de pares `m = k·(k−1)/2` (corrige a inflação do erro tipo I de testar vários pares):

     | nº de pares `m` (grupos) | t crítico de Bonferroni (~95%) |
     |---|---|
     | 1 (2 grupos) | 2,0 |
     | 3 (3 grupos) | 2,4 |
     | 6 (4 grupos) | 2,65 |
     | 10 (5 grupos) | 2,8 |

   - Um par é significativo se `t > t_crítico_Bonferroni`. **Reporte explicitamente quais pares diferem** — é isso que o post-hoc responde e a ANOVA sozinha não responde.

**Resultado final:**
- variante_vencedora conclusiva **apenas se o omnibus for significativo** (Caso B) ou o t único passar (Caso A). O vencedor segue sendo o de maior ROI com margem positiva (critério acima); o post-hoc serve para mostrar contra quais grupos a diferença é robusta.
- Se **não significativo**: variante_vencedora = "Inconclusivo", decisão = recomendar estender o teste.

### 4. Apontar trade-offs
- Volume: qual grupo tem mais compradores/dia
- Eficiência: qual grupo tem menor cashback rate
- Se o vencedor por ROI não for o de maior volume, mencionar explicitamente

### 4. Gerar relatório
- Salvar em `reports/relatorio_<Parceiro>.md`
- Formato: apresentável para um gestor, com tabela de métricas e recomendação clara
- Na seção de análise estatística, **deixe explícito o fluxo de duas etapas** para 3+ grupos: (1) o **F do omnibus** com seu veredito (há ou não diferença entre algum par) e (2) a **tabela post-hoc** mostrando, par a par, o t-score, o limiar de Bonferroni usado e se cada par é significativo. Para 2 grupos, mostre o t e o veredito únicos. Nunca rotule de "ANOVA" a soma de t-tests pareados.

### 5. Registrar na planilha

Salve em `resultados.csv` seguindo **exatamente** este formato para cada teste:

| Campo | Formato obrigatório | Exemplo |
|---|---|---|
| `nome_teste` | `dataset_<nn>_parceiro<X>` | `dataset_01_parceiroA` |
| `descricao` | `Teste de cashback com <N> variantes: G1=<x>% / G2=<y>% do GMV — <dias> dias` | `Teste de cashback com 3 variantes: G1=4,16% / G2=5,77% / G3=7,42% do GMV — 92 dias` |
| `variante_vencedora` | `Grupo <N>` ou `Inconclusivo` | `Grupo 1` |
| `decisao` | `Escalar Grupo <N>: ROI <x>x e margem <y>%. <motivo curto>.` ou `Inconclusivo: estender teste. Melhor grupo provisório: Grupo <N>` | `Escalar Grupo 1: ROI 24,0x e margem 7,22%. Cashback rate mais eficiente.` |
| `data_analise` | `YYYY-MM-DD` | `2026-06-16` |

- **Sempre envolva cada campo em aspas duplas**
- Só escreva o `resultados.csv` **uma única vez**, com todos os testes analisados juntos — nunca escreva linha por linha durante a análise
- Se o arquivo não existir, crie com o cabeçalho; se já existir, sobrescreva completamente
- O upload para o Google Sheets é feito **automaticamente** pelo hook após a escrita — não tente usar MCP nem chamar scripts manualmente

## Regras importantes
- Não use Python, scripts ou dependências externas — faça tudo com leitura e escrita de arquivos nativos
- A solução deve funcionar para QUALQUER dataset no schema padrão
- A decisão final deve responder: "Qual variante escalar para 100% do tráfego?"
- Se as diferenças entre grupos forem pequenas (< 5%), deixe isso claro no relatório

## Schema dos datasets
| Coluna | Tipo | Descrição |
|---|---|---|
| Data | YYYY-MM-DD | Data da observação |
| Grupos de usuários | string | Variante do teste |
| Parceiro | string | Parceiro do teste |
| compradores | int | Usuários únicos que compraram |
| comissão | R$ string | Comissão paga pelo parceiro ao Méliuz |
| cashback | R$ string | Cashback distribuído aos usuários |
| vendas totais | R$ string | GMV do dia |
