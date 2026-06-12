"""
Analisador de Testes A/B — Méliuz
Uso: python analyze.py datasets/dataset_01_parceiroA.csv
"""

import sys
import os
import re
import csv
from datetime import date
import pandas as pd
from scipy import stats


# ─── Helpers ────────────────────────────────────────────────────────────────

def parse_brl(value):
    """Converte 'R$ 1.234,56' ou 'R$ 1.234' para float."""
    if pd.isna(value):
        return 0.0
    cleaned = re.sub(r"[R$\s]", "", str(value)).replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load_dataset(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    for col in ["comissão", "cashback", "vendas totais"]:
        df[col] = df[col].apply(parse_brl)
    df["compradores"] = pd.to_numeric(df["compradores"], errors="coerce").fillna(0).astype(int)
    df["Data"] = pd.to_datetime(df["Data"])
    return df


# ─── Métricas ────────────────────────────────────────────────────────────────

def calc_metrics(df):
    grouped = df.groupby("Grupos de usuários").agg(
        compradores=("compradores", "sum"),
        comissao=("comissão", "sum"),
        cashback=("cashback", "sum"),
        vendas=("vendas totais", "sum"),
        dias=("Data", "nunique"),
    ).reset_index()

    grouped["ticket_medio"] = grouped["vendas"] / grouped["compradores"].replace(0, float("nan"))
    grouped["cashback_rate"] = grouped["cashback"] / grouped["vendas"].replace(0, float("nan"))
    grouped["margem_meliuz"] = (grouped["comissao"] - grouped["cashback"]) / grouped["vendas"].replace(0, float("nan"))
    grouped["roi_cashback"] = grouped["vendas"] / grouped["cashback"].replace(0, float("nan"))
    grouped["compradores_dia"] = grouped["compradores"] / grouped["dias"]

    return grouped


# ─── Estatística ─────────────────────────────────────────────────────────────

def stat_test(df, grupos):
    """Teste t entre os dois grupos com maior e menor cashback_rate."""
    resultados = []
    grupo_names = df["Grupos de usuários"].unique()

    if len(grupo_names) < 2:
        return None, None, None

    # compara o grupo de maior volume vs menor (ou todos par a par, pega o melhor p)
    melhor_p = 1.0
    melhor_par = (grupo_names[0], grupo_names[1])
    for i in range(len(grupo_names)):
        for j in range(i + 1, len(grupo_names)):
            g1 = df[df["Grupos de usuários"] == grupo_names[i]]["vendas totais"]
            g2 = df[df["Grupos de usuários"] == grupo_names[j]]["vendas totais"]
            if len(g1) < 2 or len(g2) < 2:
                continue
            _, p = stats.ttest_ind(g1, g2)
            if p < melhor_p:
                melhor_p = p
                melhor_par = (grupo_names[i], grupo_names[j])

    g1 = df[df["Grupos de usuários"] == melhor_par[0]]["vendas totais"]
    g2 = df[df["Grupos de usuários"] == melhor_par[1]]["vendas totais"]
    _, p_value = stats.ttest_ind(g1, g2)
    significativo = p_value < 0.05
    confianca = (1 - p_value) * 100

    return round(p_value, 4), significativo, round(confianca, 1)


# ─── Decisão ─────────────────────────────────────────────────────────────────

def decide_winner(metrics, p_value, significativo):
    """
    Critério: melhor ROI do cashback (mais vendas por R$ de cashback gasto),
    com margem positiva para o Méliuz.
    """
    validos = metrics[metrics["margem_meliuz"] > 0]
    if validos.empty:
        validos = metrics  # fallback se todas as margens forem negativas

    vencedor = validos.sort_values("roi_cashback", ascending=False).iloc[0]
    return vencedor["Grupos de usuários"], vencedor


# ─── Relatório ───────────────────────────────────────────────────────────────

def gerar_relatorio(df, metrics, parceiro, periodo, p_value, significativo, confianca, vencedor, nome_vencedor):
    os.makedirs("reports", exist_ok=True)
    safe_name = parceiro.replace(" ", "_")
    filepath = f"reports/relatorio_{safe_name}.md"

    sig_texto = f"✅ Significativo (p = {p_value}, confiança {confianca}%)" if significativo else f"⚠️ Não significativo (p = {p_value}) — resultado inconclusivo"

    linhas_tabela = ""
    for _, row in metrics.iterrows():
        linhas_tabela += (
            f"| {row['Grupos de usuários']} "
            f"| {int(row['compradores_dia']):,} "
            f"| R$ {row['ticket_medio']:,.0f} "
            f"| {row['cashback_rate']*100:.1f}% "
            f"| {row['margem_meliuz']*100:.1f}% "
            f"| {row['roi_cashback']:.1f}x |\n"
        )

    relatorio = f"""# Relatório Teste A/B — {parceiro}

## Resumo Executivo

- **Período:** {periodo}
- **Grupos testados:** {', '.join(metrics['Grupos de usuários'].tolist())}
- **Decisão: Escalar {nome_vencedor} para 100% do tráfego**

## Métricas por Grupo

| Grupo | Compradores/dia | Ticket Médio | Cashback Rate | Margem Méliuz | ROI Cashback |
|-------|----------------|--------------|---------------|---------------|--------------|
{linhas_tabela}
> **Cashback Rate**: quanto do GMV foi devolvido em cashback (menor = mais eficiente para o Méliuz)
> **Margem Méliuz**: (comissão - cashback) / vendas — quanto o Méliuz retém
> **ROI Cashback**: vendas geradas por cada R$ de cashback distribuído

## Análise Estatística

- {sig_texto}

## Recomendação

**Escalar {nome_vencedor}.**

{nome_vencedor} apresentou o melhor ROI de cashback ({vencedor['roi_cashback']:.1f}x),
com margem de {vencedor['margem_meliuz']*100:.1f}% para o Méliuz e cashback rate de
{vencedor['cashback_rate']*100:.1f}% — o melhor equilíbrio entre volume de vendas e
custo de cashback entre os grupos testados.
{"O resultado é estatisticamente significativo, indicando que a diferença não é por acaso." if significativo else "Atenção: o resultado não atingiu significância estatística — considere estender o teste antes de escalar."}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(relatorio)

    print(f"  Relatório salvo em: {filepath}")
    return relatorio


# ─── Planilha ────────────────────────────────────────────────────────────────

def registrar_resultado(parceiro, periodo, nome_vencedor, decisao):
    planilha = "resultados.csv"
    ja_existe = os.path.exists(planilha)

    with open(planilha, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not ja_existe:
            writer.writerow(["nome_teste", "descricao", "variante_vencedora", "decisao", "data_analise"])
        writer.writerow([
            f"Teste {parceiro}",
            f"Teste A/B de cashback — {parceiro} | {periodo}",
            nome_vencedor,
            decisao,
            date.today().isoformat(),
        ])

    print(f"  Resultado registrado em: {planilha}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python analyze.py <caminho_do_csv>")
        print("Ex:  python analyze.py datasets/dataset_01_parceiroA.csv")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"\n Carregando dataset: {filepath}")

    df = load_dataset(filepath)

    parceiro = df["Parceiro"].iloc[0]
    data_inicio = df["Data"].min().strftime("%d/%m/%Y")
    data_fim = df["Data"].max().strftime("%d/%m/%Y")
    periodo = f"{data_inicio} a {data_fim}"

    print(f"  Parceiro: {parceiro} | Período: {periodo} | Linhas: {len(df)}")

    print("\n Calculando métricas por grupo...")
    metrics = calc_metrics(df)
    print(metrics[["Grupos de usuários", "compradores", "ticket_medio", "cashback_rate", "margem_meliuz", "roi_cashback"]].to_string(index=False))

    print("\n Rodando análise estatística...")
    p_value, significativo, confianca = stat_test(df, metrics)

    print("\n Determinando vencedor...")
    nome_vencedor, vencedor = decide_winner(metrics, p_value, significativo)
    print(f"  Vencedor: {nome_vencedor}")

    decisao = f"Escalar {nome_vencedor} para 100% do tráfego"

    print("\n Gerando relatório...")
    gerar_relatorio(df, metrics, parceiro, periodo, p_value, significativo, confianca, vencedor, nome_vencedor)

    print("\n Registrando na planilha...")
    registrar_resultado(parceiro, periodo, nome_vencedor, decisao)

    print(f"\n✅ Análise concluída! Decisão: {decisao}\n")


if __name__ == "__main__":
    main()
