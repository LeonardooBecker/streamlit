"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 08/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

import pandas as pd
import streamlit as st
import folium
import altair as alt
from local_libs.alteraNomes import *
from local_libs.calculaParametros import *
from local_libs.preencheMapa import * 
from local_libs.corrigeFiltros import *
from local_libs.titulo import *
from local_libs.rodape import *
from local_libs.radaresMapa import *

with open("./css/style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


# Inicialização dos valores de session_state, utilizado durante todo o código
def inicializaValores():
    st.session_state["HIERARQUIA_CTB"] = [""]
    st.session_state["WEEKDAY"]=[""]
    st.session_state["SEXO"] = [""]
    st.session_state["IDADE"] = [""]
    st.session_state["BAIRRO"]=[""]
    st.session_state["CIDADE"]=[""]
    st.session_state["DRIVER"] = [""]
    st.session_state["ID"] = [""]

    st.session_state["HIERARQUIA_CTBSELECT"] = ""
    st.session_state["WEEKDAYSELECT"]=""
    st.session_state["SEXOSELECT"] = ""
    st.session_state["IDADESELECT"] = ""
    st.session_state["BAIRROSELECT"]=""
    st.session_state["CIDADESELECT"]=""
    st.session_state["DRIVERSELECT"] = ""
    st.session_state["IDSELECT"] = ""

    st.session_state["ESCOLHA"] = "Frequência de uso do celular (usos/hora)"
    st.session_state["VELOCIDADE"]=True

def main():
    my_map = folium.Map(location=[-25.442027, -49.269582],
                            zoom_start=12,tiles='CartoDB positron')

    map_radar = folium.Map(location=[-25.442027, -49.269582],
                        zoom_start=12)

    tabela = pd.read_csv("./data/AllFullTable.csv", sep=";", low_memory=False)

    # Inicialização dos valores
    if "VELOCIDADE" not in st.session_state:
        inicializaValores()

    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario={
        "HIERARQUIA_CTB":st.session_state["HIERARQUIA_CTBSELECT"],
        "WEEKDAY":st.session_state["WEEKDAYSELECT"],
        "SEXO":st.session_state["SEXOSELECT"],
        "IDADE":st.session_state["IDADESELECT"],
        "BAIRRO":st.session_state["BAIRROSELECT"],
        "CIDADE":st.session_state["CIDADESELECT"],
        "DRIVER":st.session_state["DRIVERSELECT"],
        "ID":st.session_state["IDSELECT"]
        }

    preencheVetorFiltro(dicionario,tabela)

    # Painel lateral - cada linha corresponde a um filtro possível
    for chave in dicionario:
        chaveSelect=chave+"SELECT"
        if(chave=="SEXO"):
            st.session_state[chaveSelect]=st.sidebar.radio(formataNome(chave),st.session_state[chave])
        elif(chave=="HIERARQUIA_CTB"):
            st.session_state[chaveSelect]=desconverteSing(st.sidebar.selectbox(formataNome(chave),st.session_state[chave]))
        elif(chave=="WEEKDAY"):
            st.session_state[chaveSelect]=st.sidebar.selectbox(formataNome(chave),transformaWeekday(st.session_state[chave]))
        else:
            st.session_state[chaveSelect]=st.sidebar.selectbox(formataNome(chave),st.session_state[chave])

    # Atualização extra necessária para deixar os parâmetros do filtro de acordo
    for chave in dicionario:
        if(dicionario[chave]!=st.session_state[chave+"SELECT"]):
            st.experimental_rerun()

    # Botão de atualização da página
    if st.sidebar.button('Atualizar página'):
        st.session_state.clear()
        st.experimental_rerun()

    ## Título da página
    titulo("Estudo Naturalístico de Direção Brasileiro - Indicadores sobre excesso de velocidade")

    #---------------------------------------------
    separaConteudo()

    # Cálculo e apresentaçao dos parâmetros na box superior
    tabelaFiltrada=atualizaTabela(dicionario,tabela)
    tempoValido=calculaTempoValido(tabelaFiltrada)
    percentualExcesso = calculaPercentualExcesso(tabelaFiltrada,tempoValido)
    percentualOportunidade=calculaOportunidadeExcesso(tabelaFiltrada,tempoValido)
    percentualExcessoCorrigido = calculaPercentualExcessoCorrigido(tabelaFiltrada)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Percentual do tempo sob excesso de velocidade em relação ao tempo total de viagem", str(
            percentualExcesso)+"%")
    with col2:
        st.metric("Percentual do tempo de viagem com oportunidade de excesso de velocidade", str(
            percentualOportunidade)+"%")
    with col3:
        st.metric("Percentual do tempo sob excesso de velocidade em relação ao tempo de viagem*",
                str(percentualExcessoCorrigido)+"%")
        
    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Cidades
    cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str).tolist()
    percentCidades = []
    cidadesOfc = []
    for cidade in cidades:
        dfCidade = tabelaFiltrada[tabelaFiltrada["CIDADE"] == cidade]
        excessoCorrigido=calculaPercentualExcessoCorrigido(dfCidade)
        if (excessoCorrigido > 0):
            percentCidades.append(excessoCorrigido)
            cidadesOfc.append(cidade)


    data = {"Cidade": cidadesOfc, "Percentual": percentCidades}
    new_df = pd.DataFrame(data)
    dfCidade = new_df.sort_values(["Percentual"])

    st.subheader("Percentual do tempo sob excesso de velocidade por cidade*")
    bars = alt.Chart(dfCidade).mark_bar(width=20).encode(
        x='Percentual',
        y=alt.Y("Cidade", sort='x')
    )
    st.altair_chart(bars)

    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Bairros
    bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str).tolist()
    percentBairros = []
    bairrosOfc = []

    for bairro in bairros:
        dfBairro = tabelaFiltrada[tabelaFiltrada["BAIRRO"] == bairro]
        excessoCorrigido=calculaPercentualExcessoCorrigido(dfBairro)
        if (excessoCorrigido > 0):
            percentBairros.append(excessoCorrigido)
            bairrosOfc.append(bairro)

    data = {"Bairro": bairrosOfc, "Percentual": percentBairros}
    new_df = pd.DataFrame(data)
    dfBairro = new_df.sort_values(["Percentual"])

    st.subheader("Percentual do tempo sob excesso de velocidade por bairro de Curitiba*")
    bars = alt.Chart(dfBairro).mark_bar(width=20).encode(
        x='Percentual',
        y=alt.Y("Bairro", sort='x')
    )
    st.altair_chart(bars)

    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Limite de velocidade
    limites = ((pd.Series.unique(tabela["LIMITE_VEL"]))).astype(str).tolist()
    percentVia = []
    limiteVias = []

    for limite in limites:
        dfLm = tabelaFiltrada[tabelaFiltrada["LIMITE_VEL"] == int(limite)]
        excessoCorrigido=calculaPercentualExcessoCorrigido(dfLm)
        if (excessoCorrigido > 0):
            percentVia.append(excessoCorrigido)
            limiteVias.append(limite)

    data = {"Limite da via": limiteVias, "Percentual": percentVia}
    new_df = pd.DataFrame(data)
    dfLimite = new_df.sort_values(["Percentual"])

    st.subheader("Percentual do tempo sob excesso de velocidade segundo limite de velocidade regulamentar da via*")
    bars = alt.Chart(dfLimite).mark_bar(width=20).encode(
        x='Percentual',
        y=alt.Y("Limite da via", sort='-x')
    )
    st.altair_chart(bars)

    #---------------------------------------------
    separaConteudo()

    # Inserção do mapa e coloração do mapa sobre velocidade localizado na parte inferior da página
    coloreMapa("Percentual do tempo sob excesso de velocidade*",tabelaFiltrada,my_map)
    insereMapa("Percentual do tempo sob excesso de velocidade*",my_map)

    #---------------------------------------------
    separaConteudo()

    # Inserção do mapa e coloração do mapa sobre radares localizado na parte inferior da página
    insereMapaRadar(map_radar)

    #---------------------------------------------

    separaConteudo()
    ## Rodapé da página
    rodape()

if __name__ == "__main__":
    main()