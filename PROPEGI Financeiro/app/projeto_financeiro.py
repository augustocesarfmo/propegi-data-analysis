import streamlit as st

st.set_page_config(page_title="PROPEGI Financeiro", page_icon="../../images/upeLogo.png", layout="wide", initial_sidebar_state="collapsed")
st.title("Home")
st.write("Use os links abaixo para navegar:")

st.page_link("projeto_financeiro.py", label="Home", icon="🏠")
st.page_link("analisesFinanceiras/analise1_comparativa.py", label="Análise 1 — Comparativo de Valores das Folhas por Projeto", icon="1️⃣")
st.page_link("analisesFinanceiras/analise2_somatorio.py", label="Análise 2 — Somatório de Valores das Folhas", icon="2️⃣")
st.page_link("analisesFinanceiras/analise3_total_mensal.py", label="Análise 3 — Total Mensal de Projetos", icon="3️⃣")