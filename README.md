# PPL-SOLVER

Solucionador de Problemas de Programação Linear (PPL) em Python.

Este projeto fornece uma interface web (Streamlit) para modelar e resolver problemas de programação
linear usando a biblioteca PuLP. Além da solução ótima, a aplicação apresenta informações de
análise de sensibilidade como preços-sombra e folgas (slacks).

## Estrutura do repositório

- `app.py` — entrada principal da interface Streamlit
- `static/styles.css` — estilos CSS usados pela interface
- `solver/` — pacote do resolvedor
  - `solver/solver.py` — função `solve_lp(...)` que monta e resolve o modelo usando PuLP
  - `solver/__init__.py` — expõe `solve_lp` para importações simples
- `requirements.txt` — dependências Python (Streamlit, PuLP, pandas, etc.)
- `setup_env.sh` — script auxiliar para criar ambiente (opcional)

## Pré-requisitos

- Python 3.8+

Recomendado usar um ambiente virtual (venv or conda).

## Instalação rápida

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se preferir, execute o script `setup_env.sh`

## Como executar

```bash
streamlit run app.py
```

## Autores

Feito por Petterson Ikaro e Luis Otavio Amante
