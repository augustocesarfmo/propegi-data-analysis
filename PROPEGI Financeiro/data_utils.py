from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

# Meus Meses na ordem certa (1..12)
MESES = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}

def _to_float(valor):
    """
    Converte '32617,27' -> 32617.27 e mantém números já numéricos.
    Também lida com None/vazio retornando 0.0 para evitar quebras.
    """
    if valor is None: #Tratei para caso venha Valor da folha como None
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    txt = str(valor).strip().replace(".", "")  # Se caso venha separador de milhar, o que é raro
    txt = txt.replace(",", ".")
    try:
        return float(txt)
    except ValueError:
        return 0.0

def carregar_financas_json(caminho_arquivo: str | Path) -> pd.DataFrame:
    """
    Lê o JSON de finanças e devolve um DataFrame com:
    - 'Projetos', 'Ano', 'Mês', 'Número do mês', 'Valor da folha' (float)
    - coluna extra 'AnoMes' no formato '2021-Jan' (ordenável por 'Número do mês')
    """
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho.resolve()}")

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    df = pd.DataFrame(dados)

    # Parte responsável por garantir colunas essenciais
    colunas_essenciais = ["Projetos", "Ano", "Mês", "Número do mês", "Valor da folha"]
    faltando = [c for c in colunas_essenciais if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes no JSON: {faltando}")

    # Normaliza valores
    df["Valor da folha"] = df["Valor da folha"].apply(_to_float)

    # Cria rótulo Ano-Mês ordenável
    df["MesAbrev"] = df["Número do mês"].map(MESES).fillna(df["Mês"])
    df["AnoMes"] = df["Ano"].astype(str) + "-" + df["MesAbrev"].astype(str)
    df["ord_col"] = df["Ano"] * 100 + df["Número do mês"]  # Para ordenação correta nas colunas do heatmap

    return df

def filtrar(df: pd.DataFrame, anos: list[int] | None, projetos: list[str] | None) -> pd.DataFrame:
    """Aplica filtros simples por ano e projetos (se fornecidos)."""
    out = df.copy()
    if anos:
        out = out[out["Ano"].isin(anos)]
    if projetos:
        out = out[out["Projetos"].isin(projetos)]
    return out

# Importante: função usada para as análises de Taxa e Plano de Trabalho
def somatorio_por_taxa_plano(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa e soma 'Valor da folha' por projeto, taxa e plano de trabalho.
    Garante que as colunas 'Taxa' e 'Plano de Trabalho' existam.
    Retorna DataFrame pronto para exportar como JSON.
    """
    df = df.copy()
    if "Taxa" not in df.columns: #Serve para evitar erro se a coluna taxa não existir
        df["Taxa"] = "N/A"
    if "Plano de Trabalho" not in df.columns: #Serve para evitar erro se a coluna plano de trabalho não existir
        df["Plano de Trabalho"] = "N/A"

    agrupado = df.groupby([
        "Projeto_ID", "Projetos", "Projeto de Origem", "Ano", "Mês", "Número do mês", "Taxa", "Plano de Trabalho"
    ], dropna=False, as_index=False)["Valor da folha"].sum()
    return agrupado