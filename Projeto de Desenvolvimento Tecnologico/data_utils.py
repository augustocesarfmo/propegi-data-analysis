from __future__ import annotations
from pathlib import Path
import pandas as pd

# Raiz do projeto (pasta onde está este arquivo)
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"

# Nome padrão do JSON (ajuste se necessário)
DEFAULT_JSON_NAME = "Projetos de Desenvolvimento Tecnologico.json"
BRL_COLS = ["Valor agência", "Valor unidade", "Valor IA-UPE"]

def input_path(name: str | Path = DEFAULT_JSON_NAME) -> Path:
    """Retorna o caminho absoluto dentro de input/."""
    p = INPUT_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"Arquivo não encontrado em: {p}")
    return p

def carregar_json(path: str | Path | None = None) -> pd.DataFrame:
    """
    Lê o JSON (lista de objetos) e retorna um DataFrame.
    Se path for None, usa input/DEFAULT_JSON_NAME.
    """
    if path is None:
        path = input_path(DEFAULT_JSON_NAME)
    return pd.read_json(path)

def _br_to_float(serie: pd.Series) -> pd.Series:
    """
    Converte '1.234.567,89' -> 1234567.89. Aceita também numérico.
    """
    if pd.api.types.is_numeric_dtype(serie):
        return serie.astype(float)
    serie = (
        serie.fillna("0")
             .astype(str)
             .str.replace(".", "", regex=False)
             .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(serie, errors="coerce").fillna(0.0)

def normalizar_valores(df: pd.DataFrame) -> pd.DataFrame:
    """Garante que colunas monetárias estejam em float."""
    for c in BRL_COLS:
        if c in df.columns:
            df[c] = _br_to_float(df[c])
    return df

def preparar_datas(df: pd.DataFrame) -> pd.DataFrame:
    """Converte 'Data publicação' e cria colunas Ano/Mes/MesNome."""
    df = df.copy()
    df["Data publicação"] = pd.to_datetime(df["Data publicação"], dayfirst=True, errors="coerce")
    df["Ano"] = df["Data publicação"].dt.year
    df["Mes"] = df["Data publicação"].dt.month
    df["MesNome"] = df["Data publicação"].dt.strftime("%m/%b")
    return df

def agrupar_mensal(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    """Soma por mês (1..12) os valores da agência, unidade e IA-UPE para o ano dado."""
    df_ano = df[df["Ano"] == ano].copy()
    if df_ano.empty:
        base = pd.DataFrame({"Mes": range(1, 13)})
        base["MesNome"] = base["Mes"].apply(lambda m: pd.Timestamp(year=ano, month=m, day=1).strftime("%m/%b"))
        for c in BRL_COLS:
            base[c] = 0.0
        return base

    grp = (
        df_ano.groupby(["Mes", "MesNome"], as_index=False)[BRL_COLS]
        .sum()
        .sort_values("Mes")
    )
    meses_completos = pd.DataFrame({"Mes": range(1, 13)})
    meses_completos["MesNome"] = meses_completos["Mes"].apply(
        lambda m: pd.Timestamp(year=ano, month=m, day=1).strftime("%m/%b")
    )
    out = meses_completos.merge(grp, on=["Mes", "MesNome"], how="left").fillna(0.0)
    return out

def kpis_anuais(df_mes: pd.DataFrame) -> dict:
    """Totais do ano (soma dos meses) para cards."""
    return {
        "agencia": float(df_mes["Valor agência"].sum()) if "Valor agência" in df_mes else 0.0,
        "unidade": float(df_mes["Valor unidade"].sum()) if "Valor unidade" in df_mes else 0.0,
        "ia_upe": float(df_mes["Valor IA-UPE"].sum()) if "Valor IA-UPE" in df_mes else 0.0,
    }

def brl(v: float) -> str:
    """Formata float para BRL simples (R$ 1.234,56)."""
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"
