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

Liste todos os arquivos `.csv` encontrados em `datasets/`, numerados, e pergunte ao usuário quais deseja analisar antes de começar. Aguarde a resposta antes de prosseguir.

## O que você deve fazer (sempre nessa ordem)

### 1. Ler os dados
- Ler cada CSV diretamente com a ferramenta de leitura de arquivos
- Identificar os grupos de usuários, parceiro e período do teste

### 2. Calcular métricas por grupo
Para cada variante (Grupo 1, Grupo 2, etc.), calcule:
- **Ticket médio**: vendas totais / compradores
- **Cashback rate**: cashback / vendas totais — custo para o Méliuz (menor = melhor)
- **Margem do Méliuz**: (comissão - cashback) / vendas totais
- **ROI do cashback**: vendas totais / cashback — retorno por R$ gasto (maior = melhor)
- **Compradores/dia**: média diária de compradores únicos

### 3. Comparar os grupos
- Identificar qual grupo tem melhor ROI do cashback mantendo margem positiva
- Verificar se há diferença relevante entre os grupos (variação > 10% já é significativa para decisão de negócio)
- Apontar trade-offs: volume de compradores vs eficiência do cashback

### 4. Gerar relatório
- Salvar em `reports/relatorio_<Parceiro>.md`
- Formato: apresentável para um gestor, com tabela de métricas e recomendação clara

### 5. Registrar na planilha
- Salve os resultados em `resultados.csv` (schema: `nome_teste,descricao,variante_vencedora,decisao,data_analise`)
- Se o arquivo não existir, crie com o cabeçalho; se já existir, sobrescreva com todos os testes analisados
- O upload para o Google Sheets é feito **automaticamente** pelo hook configurado em `.claude/settings.json` — não tente usar MCP nem chamar scripts manualmente

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
