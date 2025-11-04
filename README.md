# ◈ Data Analysis UPE

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20.0-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Dashboards interativos em **Streamlit** que consomem arquivos **JSON** para dois domínios principais:

- **PROPEGI Financeiro**
- **Projeto de Desenvolvimento Tecnológico**

Este README foi reescrito para mostrar, passo a passo, como preparar o ambiente e executar os dois apps localmente — com instruções para PowerShell (Windows), shells Unix (bash/zsh) e `fish`.

---

## Requisitos

- Python 3.10+ (recomendado)
- Git (opcional para clonar)
- Dependências do projeto listadas em `requirements.txt`

Observação: o projeto usa principalmente `streamlit`, `pandas`, `plotly` e `numpy`.

---

## 1) Clonar o repositório

```powershell
git clone https://github.com/propegi-upe/propegi-data-analysis.git
cd 'propegi-data-analysis'
```

---

## 2) Criar e ativar ambiente virtual (OBRIGATÓRIO)

⚠️ **IMPORTANTE**: É obrigatório usar um ambiente virtual para evitar conflitos com outros projetos Python.
Vamos criar um ambiente chamado `.venv` na raiz do repositório.

Windows (PowerShell):

```powershell
python -m venv .venv
# Ativar (PowerShell)
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução do script de ativação por política de execução, rode (apenas para a sessão atual):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Confirm:$false
```

Linux / macOS (bash / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

fish shell (ex.: quando o professor pediu para usar `fish`):

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
```

---

## 3) Instalar dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

Se precisar de pacotes de desenvolvimento (formatadores, linter, testes), posso adicionar `requirements-dev.txt` — me avise.

---

## 4) Estrutura relevante do projeto

- `Projeto de Desenvolvimento Tecnologico/`
  - `app.py` — app Streamlit principal deste domínio
  - `data_utils.py`, `pages/` — utilitários e páginas auxiliares
  - `input/Projetos de Desenvolvimento Tecnologico.json` — exemplo/entrada de dados

- `PROPEGI Financeiro/`
  - `app.py` — app Streamlit principal do domínio financeiro
  - `data_utils.py`, `pages/` — utilitários e páginas auxiliares
  - `input/Financas.json` — arquivo de dados financeiros

---

## 5) Como executar os apps (exemplos)

⚠️ **MUITO IMPORTANTE**: 
1. **SEMPRE** ative o ambiente virtual (`.venv`) antes de rodar (veja passo 2)
2. **NUNCA** tente rodar sem ativar o ambiente virtual, pois as dependências não estarão disponíveis
3. **O MESMO** ambiente virtual (`.venv`) serve para rodar os dois projetos! Não precisa criar um novo

💡 **Dica**: Depois que o ambiente virtual estiver ativado, você pode rodar qualquer um dos dois projetos (ou os dois ao mesmo tempo em terminais diferentes)!

PowerShell (Windows) — PROPEGI Financeiro:

```powershell
cd 'c:\Users\Elward\Documents\repositorios\propegi-data-analysis\PROPEGI Financeiro'
streamlit run app.py
```

PowerShell (Windows) — Projeto de Desenvolvimento Tecnologico:

```powershell
cd 'c:\Users\Elward\Documents\repositorios\propegi-data-analysis\Projeto de Desenvolvimento Tecnologico'
streamlit run app.py
```

fish / bash / zsh (Unix-like) — exemplo (ajuste o caminho):

```bash
cd 'PROPEGI Financeiro'
streamlit run app.py
```

Observação: os caminhos acima assumem que você está na máquina local onde o repositório foi clonado. Ajuste os caminhos conforme sua organização de pastas.

---

## 6) Dicas rápidas / resolução de problemas

- Erro "module not found" para `streamlit` ou `pandas`:
  - **Causa mais comum**: ambiente virtual não está ativado
  - **Solução**: 
    1. Ative o ambiente virtual (`.venv`) seguindo o passo 2
    2. Execute `pip install -r requirements.txt` novamente
    3. Confirme que está ativado verificando se aparece `(.venv)` no início do prompt
- Erro ao ativar `.venv` no PowerShell:
  - Execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Confirm:$false` na sessão atual e tente ativar novamente.
- Arquivo JSON não encontrado:
  - Verifique que os arquivos JSON (`input/*.json`) estejam na pasta `input/` correspondente. As páginas usam `input_path()` e `DEFAULT_JSON_NAME` para localizar o arquivo.
- Selectbox com lista vazia (Streamlit):
  - Se uma página usa `st.selectbox(..., index=0)` e não existem opções, Streamlit pode lançar erro. Caso veja esse erro, me peça que eu ajuste o código para checar lista vazia antes de criar o componente.

---

## 7) Quero ajuda para (opções)

- Gerar `requirements-dev.txt` com `black`, `flake8`, `pytest` e um `Makefile` simples.
- Inserir testes básicos (`pytest`) para as funções de parsing/normalização.
- Corrigir pequenos bugs de UX (ex.: `selectbox` quando não há anos disponíveis).

Diga qual opção prefere que eu implemente primeiro e eu procedo com as mudanças.

---

## Licença

Distribuído sob a licença MIT — veja `LICENSE` para detalhes.
