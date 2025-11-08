import os
import streamlit as st
import pandas as pd
from solver.solver import solve_lp

_ICON_PATH = os.path.join(os.path.dirname(__file__), "image.png")
st.set_page_config(page_title="LP Solver", layout="centered", page_icon=_ICON_PATH)

css_path = os.path.join(os.path.dirname(__file__), "static", "styles.css")
with open(css_path, "r", encoding="utf-8") as _css:
    css_content = _css.read()
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with st.container():
    st.title("Solucionador de Programação Linear")
    st.write("Resolva problemas de maximização ou minimização utilizando o método Simplex (PuLP).")

    st.markdown("---")

    with st.expander("Configurações Iniciais", expanded=True):
        options = {"Máximização": "max", "Minimização": "min"}
        sense_label = st.radio("Tipo de problema:", list(options.keys()), horizontal=True)
        sense = options[sense_label]

        col1, col2 = st.columns(2)
        n_vars = col1.number_input("Número de variáveis:", 1, 20, 3)
        n_cons = col2.number_input("Número de restrições:", 1, 20, 3)

    st.markdown("---")

    with st.expander("Função Objetivo", expanded=True):
        c = []
        cols = st.columns(n_vars)
        for i in range(n_vars):
            c.append(cols[i].number_input(f"Coeficiente c{i+1}", value=1.0, step=0.1))

    st.markdown("---")

    with st.expander("Restrições", expanded=True):
        A, b, signs = [], [], []
        for i in range(n_cons):
            cols = st.columns(n_vars + 2)
            linha = [cols[j].number_input(f"a{i+1}{j+1}", value=1.0, step=0.1, key=f"a_{i}_{j}") for j in range(n_vars)]
            A.append(linha)
            signs.append(cols[-2].selectbox("Sinal", ["<=", ">=", "="], key=f"sign_{i}"))
            b.append(cols[-1].number_input(f"b{i+1}", value=1.0, step=0.1, key=f"b_{i}"))

    st.markdown("---")

    if st.button("Resolver"):
        result = solve_lp(c, A, b, signs, sense)

        st.header("Resultados")


        if result["status"] == "Optimal":
            st.success("Solução ótima encontrada.")


            st.markdown("\n")
            st.metric(label="Valor ótimo (Z)", value=f"{result['z_opt']:.3f}")


            st.subheader("Variáveis de decisão")
            var_names = [f"x{i+1}" for i in range(len(result["x_opt"]))]
            var_values = [round(v, 3) for v in result["x_opt"]]
            df_vars = pd.DataFrame({"Variável": var_names, "Valor": var_values})
            df_vars = df_vars.set_index("Variável")
            st.table(df_vars)


            st.subheader("Preços-sombra e folgas")
            sombra = [round(v, 3) for v in result.get("sombra", [])]
            folga = [round(v, 3) for v in result.get("folga", [])]
            cons = [f"Restrição {i+1}" for i in range(max(len(sombra), len(folga)))]
            df_cons = pd.DataFrame({"Restrição": cons, "Preço-sombra (π)": sombra + [None] * (len(cons) - len(sombra)), "Folga": folga + [None] * (len(cons) - len(folga))})
            df_cons = df_cons.set_index("Restrição")
            st.table(df_cons)
        else:
            st.error(f"Status: {result['status']}")

st.markdown("<div class='site-footer'>&copy; Feito por Petterson Ikaro e Luis Otavio Amante</div>", unsafe_allow_html=True)
