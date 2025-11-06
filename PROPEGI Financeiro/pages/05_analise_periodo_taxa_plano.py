"""
Página: Análise — Período completo por Taxa e Plano de Trabalho
Mostra o somatório no período selecionado (todas as competências incluídas no filtro), com cortes por Taxa e por Plano de Trabalho,
além de tabela por par (Taxa × Plano de Trabalho).
"""
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

# Permitir import do módulo raiz
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_utils import carregar_financas_json, filtrar  # noqa: E402

CAMINHO_PADRAO_JSON = Path(__file__).resolve().parents[1] / "input" / "Financas.json"

st.set_page_config(page_title="Análise do Período — Taxa/Plano", layout="wide", initial_sidebar_state="collapsed")
st.header("◈ Análise do Período Completo por Taxa e Plano de Trabalho")

caminho = st.text_input(
    "Caminho do arquivo Financas.json",
    value=str(CAMINHO_PADRAO_JSON),
    help="Se necessário, ajuste para o local onde o arquivo está.",
)

try:
    df = carregar_financas_json(caminho)
except Exception as e:
    st.error(f"Erro ao carregar JSON: {e}")
    st.stop()

# Filtros
anos = sorted(df["Ano"].unique().tolist())
projetos = sorted(df["Projetos"].unique().tolist())

col1, col2 = st.columns([2, 2])
with col1:
    anos_sel = st.multiselect("Filtrar por ano", anos, default=anos)
with col2:
    projeto_sel = st.selectbox("Selecionar projeto (opcional)", options=["(Todos)"] + projetos, index=0)

df_filt = filtrar(df, anos_sel, None)
if projeto_sel != "(Todos)":
    df_filt = df_filt[df_filt["Projetos"] == projeto_sel]

if df_filt.empty:
    st.warning("Sem dados para os filtros escolhidos.")
    st.stop()

# Gráfico por Taxa (período)
tot_taxa = (
    df_filt.groupby(["Taxa"], as_index=False)["Valor da folha"].sum()
    .rename(columns={"Valor da folha": "Total"})
    .sort_values("Total", ascending=False)
)
fig_taxa = px.bar(tot_taxa, x="Taxa", y="Total", text="Total", labels={"Total": "Total (R$)"}, title="Total do período por taxa")
fig_taxa.update_traces(texttemplate="R$ %{y:,.2f}")
fig_taxa.update_layout(yaxis_tickformat=",.2f", height=500)

# Gráfico por Plano de Trabalho (período)
tot_plano = (
    df_filt.groupby(["Plano de Trabalho"], as_index=False)["Valor da folha"].sum()
    .rename(columns={"Valor da folha": "Total"})
    .sort_values("Total", ascending=False)
)
fig_plano = px.bar(tot_plano, x="Plano de Trabalho", y="Total", text="Total", labels={"Total": "Total (R$)"}, title="Total do período por plano de trabalho")
fig_plano.update_traces(texttemplate="R$ %{y:,.2f}")
fig_plano.update_layout(yaxis_tickformat=",.2f", height=500)

colA, colB = st.columns(2)
with colA:
    st.subheader("Período por taxa")
    st.plotly_chart(fig_taxa, use_container_width=True)
with colB:
    st.subheader("Período por plano de trabalho")
    st.plotly_chart(fig_plano, use_container_width=True)

st.subheader("◆ Tabela — Total do período por Taxa × Plano de Trabalho")
tot_par = (
    df_filt.groupby(["Taxa", "Plano de Trabalho"], as_index=False)["Valor da folha"].sum()
    .rename(columns={"Valor da folha": "Total"})
    .sort_values(["Taxa", "Plano de Trabalho"]) 
)
st.dataframe(tot_par.style.format({"Total": "{:,.2f}"}), use_container_width=True, height=450)
