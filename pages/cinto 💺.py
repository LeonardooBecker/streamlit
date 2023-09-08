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

with open("./css/style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

# Inicialização dos valores de session_state, utilizado durante todo o código
def inicializaValores():
    st.session_state["IDADE"] = [""]
    st.session_state["SEXO"] = [""]
    st.session_state["DRIVER"] = [""]
    st.session_state["ID"] = [""]

    st.session_state["IDADESELECT"] = ""
    st.session_state["SEXOSELECT"] = ""
    st.session_state["DRIVERSELECT"] = ""
    st.session_state["IDSELECT"] = ""

    st.session_state["ESCOLHA"] = "Frequência de uso do celular (usos/hora)"
    st.session_state["CINTO"]=True

def main():
    my_map = folium.Map(location=[-25.442027, -49.269582],
                            zoom_start=12,tiles='CartoDB positron')

    tabela = pd.read_csv("./data/AllFullTable.csv", sep=";", low_memory=False)


    # Inicialização dos valores
    if "CINTO" not in st.session_state:
        inicializaValores()


    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario={
        "IDADE":st.session_state["IDADESELECT"],
        "SEXO":st.session_state["SEXOSELECT"],
        "DRIVER":st.session_state["DRIVERSELECT"],
        "ID":st.session_state["IDSELECT"]
        }

    preencheVetorFiltro(dicionario,tabela)

    # Painel lateral - cada linha corresponde a um filtro possível
    for chave in dicionario:
        chaveSelect=chave+"SELECT"
        if(chave=="SEXO"):
            st.session_state[chaveSelect]=st.sidebar.radio(formataNome(chave),st.session_state[chave])
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

    titulo("Estudo Naturalístico de Direção Brasileiro - Indicadores sobre o uso do cinto de segurança")

    ##---------------------------------------------
    separaConteudo()

    # Calculo e apresentação dos indicadores na box superior
    tabelaFiltrada=atualizaTabela(dicionario,tabela)
    percentWsb=calculaPercentWSB(tabelaFiltrada,calculaTempoValido(tabelaFiltrada))
    vmUsoCinto=calculaVMusoCinto(tabelaFiltrada)
    vmSemCinto=calculaVMsemCinto(tabelaFiltrada)

    col1, col2, col3= st.columns(3)
    with col1:
        st.metric("Percentual do tempo de não uso do cinto de segurança", str(percentWsb)+"%")
    with col2:
        st.metric("Velocidade média com o uso do cinto (km/h)", vmUsoCinto)
    with col3:
        st.metric("Velocidade média sem o uso do cinto (km/h)", vmSemCinto)
        
    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Hierarquia viária
    hierarquias = ((pd.Series.unique(tabela["HIERARQUIA_CTB"]))).astype(str).tolist()
    hctbs=[]
    percentHctbs=[]
    for hierarquia in hierarquias:
        dfHierarquiaAtual = tabelaFiltrada[tabelaFiltrada["HIERARQUIA_CTB"] == hierarquia]

        percentWsb=calculaPercentWSB(dfHierarquiaAtual,calculaTempoValido(dfHierarquiaAtual))
        percentHctbs.append(percentWsb)
        hctbs.append(converte(hierarquia)[0])


    st.subheader("Percentual do tempo de viagem sem uso do cinto segundo hierarquia da via")
    df=pd.DataFrame({"Hierarquia":hctbs, "Percentual sem cinto":percentHctbs})
    df = df.set_index("Hierarquia")
    bar_chart=st.bar_chart(df)

    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Cidades
    cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str).tolist()
    percentCidades = []
    cidadesOfc = []

    for cidade in cidades:
        dfCidade = tabelaFiltrada[tabelaFiltrada["CIDADE"] == cidade]
        percentWsb=calculaPercentWSB(dfCidade,calculaTempoValido(dfCidade))
        if(percentWsb>0 and percentWsb<100):
            cidadesOfc.append(cidade)
            percentCidades.append(percentWsb)

    data = {"Cidade": cidadesOfc, "Percentual": percentCidades}
    new_df = pd.DataFrame(data)
    dfCidade = new_df.sort_values(["Percentual"])

    st.subheader("Percentual do tempo de viagem sem o uso do cinto de segurança segundo cidade")
    bars = alt.Chart(dfCidade).mark_bar(width=20).encode(
        x='Percentual',
        y=alt.Y("Cidade",sort='x') 
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
        percentWsb=calculaPercentWSB(dfBairro,calculaTempoValido(dfBairro))
        if(percentWsb>0 and percentWsb<100):
            bairrosOfc.append(bairro)
            percentBairros.append(percentWsb)

    data = {"Bairro": bairrosOfc, "Percentual": percentBairros}

    new_df = pd.DataFrame(data)
    dfBairro = new_df.sort_values(["Percentual"])

    st.subheader("Percentual do tempo de viagem sem o uso do cinto de segurança segundo bairro")
    bars = alt.Chart(dfBairro).mark_bar(width=20).encode(
        x='Percentual',
        y=alt.Y("Bairro",sort='x') 
    )
    st.altair_chart(bars)

    #---------------------------------------------
    separaConteudo()

    # Inserção do mapa e coloração do mapa localizado na parte inferior da página
    st.subheader("Percentual do tempo de viagem sem o uso do cinto de segurança para bairros de Curitiba")
    options=["Independente do limite","Abaixo do limite","Acima do limite"]
    escolhaLimite=st.radio("Segundo limite de velocidade:",options)

    coloreMapa(escolhaLimite,tabelaFiltrada,my_map)
    insereMapa(escolhaLimite,my_map)

    #---------------------------------------------
    separaConteudo()

    # Rodapé da página
    rodape()

if __name__ == "__main__":
    main()