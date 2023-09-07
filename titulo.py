import streamlit as st

def titulo(titulo):
    # Use o f-string para inserir a variável no código HTML
    html_code = f"""
                <style>
                .titulo {{
                    display: flex;
                }}
                #texto{{
                    padding: 10px;
                }}
                #logoNDS {{
                    display: block;
                    width: 40%;
                    height: fit-content;
                    margin: auto;
                    padding: 15px;
                }}
                </style>
                <div class="titulo">
                    <h1 style="font-size:42px; text-align:center">{titulo}</h1>
                    <img src='https://www.inf.ufpr.br/lbo21/images/logoBranca.png' id="logoNDS">
                </div>
                <hr>
                """

    st.markdown(html_code, unsafe_allow_html=True)