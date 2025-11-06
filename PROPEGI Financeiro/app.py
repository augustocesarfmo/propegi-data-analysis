import streamlit as st

st.set_page_config(page_title="PROPEGI Financeiro", page_icon="../../images/upeLogo.png", layout="wide", initial_sidebar_state="collapsed")
st.title("Home")
st.write("Use os links abaixo para navegar:")

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/01_analise1_comparativa.py", label="Análise 1 — Comparativo (Heatmap)", icon="1️⃣")
st.page_link("pages/02_analise2_somatorio.py", label="Análise 2 — Somatório por Projeto", icon="2️⃣")
st.page_link("pages/03_analise3_total_mensal.py", label="Análise 3 — Total Mensal", icon="3️⃣")
st.page_link("pages/04_analise_mensal_taxa_plano.py", label="Análise 4 — Mensal por Taxa/Plano", icon="📅")
st.page_link("pages/05_analise_periodo_taxa_plano.py", label="Análise 5 — Período por Taxa/Plano", icon="📊")