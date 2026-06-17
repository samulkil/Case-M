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
    """
    Fluxo estatístico (95% de confiança, alpha = 0.05):

      - 2 grupos: teste t de Student (comparação única, sem necessidade de
        correção para múltiplas comparações).
      - 3+ grupos: ANOVA omnibus (f_oneway) para detectar SE existe diferença
        entre algum par de grupos — reporta F e p. A ANOVA não diz ENTRE QUAIS
        grupos está a diferença; por isso, se o omnibus for significativo,
        roda-se um teste post-hoc par a par com correção de Bonferroni
        (Fisher protegido) para identificar QUAIS pares diferem.

    Retorna um dict com todos os resultados (ou None se < 2 grupos).
    """
    from itertools import combinations

    ALPHA = 0.05
    NIVEL_CONFIANCA = 95

    grupo_names = list(df["Grupos de usuários"].unique())

    if len(grupo_names) < 2:
        return None

    grupos_vendas = [
        df[df["Grupos de usuários"] == g]["vendas totais"].values
        for g in grupo_names
    ]

    n_grupos = len(grupo_names)
    resultado = {
        "n_grupos": n_grupos,
        "alpha": ALPHA,
        "confianca": NIVEL_CONFIANCA,
        "grupos": grupo_names,
    }

    if n_grupos == 2:
        t_stat, p_value = stats.ttest_ind(grupos_vendas[0], grupos_vendas[1])
        significativo = bool(p_value < ALPHA)
        resultado.update({
            "tipo": "Teste t de Student",
            "f_stat": None,
            "t_stat": round(float(abs(t_stat)), 4),
            "p_value": round(float(p_value), 4),
            "significativo": significativo,
            "pares": [{
                "a": grupo_names[0],
                "b": grupo_names[1],
                "p": round(float(p_value), 4),
                "p_ajustado": round(float(p_value), 4),  # comparação única: sem correção
                "significativo": significativo,
            }],
        })
        return resultado

    # 3+ grupos: ANOVA omnibus (F, p)
    f_stat, p_omnibus = stats.f_oneway(*grupos_vendas)
    omnibus_sig = bool(p_omnibus < ALPHA)

    # Post-hoc par a par com correção de Bonferroni.
    # Só "conta" como significativo se o omnibus também foi significativo
    # (procedimento de Fisher protegido).
    pares_idx = list(combinations(range(n_grupos), 2))
    m = len(pares_idx)
    pares = []
    for i, j in pares_idx:
        _, p = stats.ttest_ind(grupos_vendas[i], grupos_vendas[j])
        p_adj = min(float(p) * m, 1.0)  # Bonferroni
        pares.append({
            "a": grupo_names[i],
            "b": grupo_names[j],
            "p": round(float(p), 4),
            "p_ajustado": round(p_adj, 4),
            "significativo": bool(omnibus_sig and p_adj < ALPHA),
        })

    resultado.update({
        "tipo": "ANOVA omnibus + post-hoc Bonferroni",
        "f_stat": round(float(f_stat), 4),
        "t_stat": None,
        "p_value": round(float(p_omnibus), 4),  # p do omnibus
        "significativo": omnibus_sig,
        "pares": pares,
    })
    return resultado


# ─── Decisão ─────────────────────────────────────────────────────────────────

def decide_winner(metrics, significativo):
    """
    Critério: melhor ROI do cashback com margem positiva.
    Se resultado não for significativo, recomenda estender o teste em vez de escalar.
    """
    validos = metrics[metrics["margem_meliuz"] > 0]
    if validos.empty:
        validos = metrics

    vencedor = validos.sort_values("roi_cashback", ascending=False).iloc[0]
    nome = vencedor["Grupos de usuários"]

    if not significativo:
        return nome, vencedor, False  # vencedor provisório, mas inconclusivo

    return nome, vencedor, True


# ─── Relatório ───────────────────────────────────────────────────────────────

def _bloco_estatistica(stat):
    """Monta a seção 'Análise Estatística' do relatório a partir do dict stat."""
    confianca = stat["confianca"]
    significativo = stat["significativo"]

    if stat["f_stat"] is None:
        # 2 grupos — teste t
        omnibus = (
            f"**Teste:** {stat['tipo']} (comparação única, sem correção).\n\n"
            f"- t = {stat['t_stat']} | p = {stat['p_value']}\n"
            f"- {'Significativo' if significativo else 'Nao significativo'} "
            f"ao nivel de {confianca}% de confianca (alpha = {stat['alpha']})"
        )
        return omnibus

    # 3+ grupos — ANOVA omnibus + post-hoc Bonferroni
    omnibus_txt = (
        f"**Teste:** {stat['tipo']}.\n\n"
        f"**1. Omnibus (ANOVA):** F = {stat['f_stat']}, p = {stat['p_value']} → "
        f"{'há diferença significativa entre algum par de grupos' if significativo else 'nenhuma diferença significativa entre os grupos'} "
        f"(alpha = {stat['alpha']}, {confianca}% de confianca).\n\n"
        f"A ANOVA indica apenas SE existe diferença, nao entre QUAIS grupos. "
    )
    if significativo:
        omnibus_txt += "Como o omnibus foi significativo, o post-hoc abaixo identifica os pares:\n\n"
    else:
        omnibus_txt += "Como o omnibus NAO foi significativo, o post-hoc nao é interpretado (Fisher protegido).\n\n"

    omnibus_txt += "**2. Post-hoc par a par (correção de Bonferroni):**\n\n"
    omnibus_txt += "| Par | p bruto | p ajustado (Bonferroni) | Significativo? |\n"
    omnibus_txt += "|---|---|---|---|\n"
    for par in stat["pares"]:
        omnibus_txt += (
            f"| {par['a']} × {par['b']} | {par['p']} | {par['p_ajustado']} | "
            f"{'Sim' if par['significativo'] else 'Nao'} |\n"
        )
    return omnibus_txt


def gerar_relatorio(df, metrics, parceiro, periodo, stat, vencedor, nome_vencedor, conclusivo):
    os.makedirs("reports", exist_ok=True)
    safe_name = parceiro.replace(" ", "_")
    filepath = f"reports/relatorio_{safe_name}.md"

    sig_texto = _bloco_estatistica(stat)

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
- **Decisão: {("Escalar " + nome_vencedor + " para 100% do tráfego") if conclusivo else ("Inconclusivo — estender teste (melhor grupo provisório: " + nome_vencedor + ")")}**

## Métricas por Grupo

| Grupo | Compradores/dia | Ticket Médio | Cashback Rate | Margem Méliuz | ROI Cashback |
|-------|----------------|--------------|---------------|---------------|--------------|
{linhas_tabela}
> **Cashback Rate**: quanto do GMV foi devolvido em cashback (menor = mais eficiente para o Méliuz)
> **Margem Méliuz**: (comissão - cashback) / vendas — quanto o Méliuz retém
> **ROI Cashback**: vendas geradas por cada R$ de cashback distribuído

## Análise Estatística

{sig_texto}

## Recomendação

{"**Escalar " + nome_vencedor + ".**" if conclusivo else "**Inconclusivo — recomenda-se estender o teste.**"}

{nome_vencedor} apresentou o melhor ROI de cashback ({vencedor['roi_cashback']:.1f}x),
com margem de {vencedor['margem_meliuz']*100:.1f}% para o Méliuz e cashback rate de
{vencedor['cashback_rate']*100:.1f}% — o melhor equilíbrio entre volume de vendas e
custo de cashback entre os grupos testados.
{"O resultado é estatisticamente significativo (ANOVA/t-test, p < 0,05), a diferença entre grupos não é atribuível ao acaso." if conclusivo else "Atenção: a diferença entre grupos não atingiu significância estatística — escalar agora representa risco. Recomenda-se coletar mais dados antes de decidir."}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(relatorio)

    print(f"  Relatório salvo em: {filepath}")
    return relatorio


# ─── Planilha ────────────────────────────────────────────────────────────────

def registrar_resultado(parceiro, periodo, nome_vencedor, decisao, metrics, conclusivo):
    planilha = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados.csv")
    ja_existe = os.path.exists(planilha)

    # nome_teste no formato padrao: dataset_01_parceiroA
    nome_arquivo = {
        "Parceiro A": "dataset_01_parceiroA",
        "Parceiro B": "dataset_02_parceiroB",
        "Parceiro C": "dataset_03_parceiroC",
    }.get(parceiro, parceiro.replace(" ", "_"))

    # descricao no formato padrao
    n_variantes = len(metrics)
    n_dias = periodo.split(" a ")
    cashback_rates = " / ".join(
        f"G{i+1}={row['cashback_rate']*100:.2f}%".replace(".", ",")
        for i, (_, row) in enumerate(metrics.iterrows())
    )
    from datetime import datetime
    d1 = datetime.strptime(periodo.split(" a ")[0], "%d/%m/%Y")
    d2 = datetime.strptime(periodo.split(" a ")[1], "%d/%m/%Y")
    dias = (d2 - d1).days + 1
    descricao = f"Teste de cashback com {n_variantes} variantes: {cashback_rates} do GMV — {dias} dias"

    # decisao no formato padrao
    if conclusivo:
        row = metrics[metrics["Grupos de usuários"] == nome_vencedor].iloc[0]
        decisao_fmt = f"Escalar {nome_vencedor}: ROI {row['roi_cashback']:.1f}x e margem {row['margem_meliuz']*100:.2f}%. Cashback rate mais eficiente.".replace(".", ",")
    else:
        decisao_fmt = f"Inconclusivo: estender teste. Melhor grupo provisório: {nome_vencedor}"

    with open(planilha, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if not ja_existe:
            writer.writerow(["nome_teste", "descricao", "variante_vencedora", "decisao", "data_analise"])
        writer.writerow([
            nome_arquivo,
            descricao,
            nome_vencedor if conclusivo else "Inconclusivo",
            decisao_fmt,
            date.today().isoformat(),
        ])

    print(f"  Resultado registrado em: {planilha}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python analyze.py <caminho_do_csv>")
        print("Ex:  python analyze.py datasets/dataset_01_parceiroA.csv")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    filepath = sys.argv[1]
    if not os.path.isabs(filepath):
        filepath = os.path.join(script_dir, filepath)
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
    stat = stat_test(df, metrics)
    if stat["f_stat"] is not None:
        print(f"  ANOVA omnibus: F = {stat['f_stat']}, p = {stat['p_value']}")
        for par in stat["pares"]:
            print(f"    post-hoc {par['a']} x {par['b']}: p_aj = {par['p_ajustado']} ({'sig' if par['significativo'] else 'ns'})")
    else:
        print(f"  Teste t: t = {stat['t_stat']}, p = {stat['p_value']}")

    print("\n Determinando vencedor...")
    nome_vencedor, vencedor, conclusivo = decide_winner(metrics, stat["significativo"])
    print(f"  Vencedor: {nome_vencedor} ({'conclusivo' if conclusivo else 'inconclusivo — estender teste'})")

    decisao = f"Escalar {nome_vencedor} para 100% do trafego" if conclusivo else f"Inconclusivo — estender teste (melhor grupo provisorio: {nome_vencedor})"

    print("\n Gerando relatorio...")
    gerar_relatorio(df, metrics, parceiro, periodo, stat, vencedor, nome_vencedor, conclusivo)

    print("\n Registrando na planilha...")
    registrar_resultado(parceiro, periodo, nome_vencedor, decisao, metrics, conclusivo)

    print(f"\nAnalise concluida! Decisao: {decisao}\n")


if __name__ == "__main__":
    main()
