"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 08/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

# Importação dos módulos
import streamlit as st
import sys
sys.path.append('./local_libs')
from alteraNomes import *
from calculaParametros import *
from preencheMapa import *
from corrigeFiltros import *
from titulo import *
from rodape import *

# Importação do CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


# Inicialização dos valores de session_state, utilizado durante todo o código
def inicializaValores():
    st.session_state["DRIVER"] = [""]
    st.session_state["BAIRRO"] = [""]
    st.session_state["CIDADE"] = [""]
    st.session_state["IDADE"] = [""]
    st.session_state["HIERARQUIA_CWB"] = [""]
    st.session_state["HIERARQUIA_CTB"] = [""]
    st.session_state["ID"] = [""]

    st.session_state["DRIVERSELECT"] = ""
    st.session_state["BAIRROSELECT"] = ""
    st.session_state["CIDADESELECT"] = ""
    st.session_state["IDADESELECT"] = ""
    st.session_state["HIERARQUIA_CWBSELECT"] = ""
    st.session_state["HIERARQUIA_CTBSELECT"] = ""
    st.session_state["IDSELECT"] = ""

    st.session_state["ESCOLHA"] = "Frequência de uso do celular (usos/hora)"
    st.session_state["INICIO"]=True


def main():

    my_map = folium.Map(location=[-25.442027, -49.269582],
                        zoom_start=12)

    tabela = pd.read_csv("./data/AllFullTable.csv", sep=";", low_memory=False)


    # Inicialização dos valores
    if "INICIO" not in st.session_state:
        inicializaValores()


    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario={
        "IDADE":st.session_state["IDADESELECT"],
        "HIERARQUIA_CWB":st.session_state["HIERARQUIA_CWBSELECT"],
        "HIERARQUIA_CTB":st.session_state["HIERARQUIA_CTBSELECT"],
        "BAIRRO":st.session_state["BAIRROSELECT"],
        "CIDADE":st.session_state["CIDADESELECT"],
        "DRIVER":st.session_state["DRIVERSELECT"],
        "ID":st.session_state["IDSELECT"]
        }

    preencheVetorFiltro(dicionario,tabela)

    # Painel lateral
    for chave in dicionario:
        chaveSelect=chave+"SELECT"
        if(chave=="HIERARQUIA_CTB"):
            st.session_state[chaveSelect]=desconverteSing(st.sidebar.selectbox(formataNome(chave),st.session_state[chave]))
        else:
            st.session_state[chaveSelect]=st.sidebar.selectbox(formataNome(chave),st.session_state[chave])


    # Atualização extra, necessária para deixar os parâmetros do filtro de acordo
    for chave in dicionario:
        if(dicionario[chave]!=st.session_state[chave+"SELECT"]):
            st.experimental_rerun()

    # Botão de atualização da página
    if st.sidebar.button('Atualizar página'):
        st.session_state.clear()
        st.experimental_rerun()


    # Título da página

    titulo("Estudo Naturalístico de Direção Brasileiro")

    #---------------------------------------------

    separaConteudo()

    # Cálculo e apresentaçao dos parâmetros na box superior

    tabelaFiltrada=atualizaTabela(dicionario,tabela)

    tempoValido = calculaTempoValido(tabelaFiltrada)

    freqUsoCelular=calculaFreqUsoCelular(tabelaFiltrada,tempoValido)

    percentWsb=calculaPercentWSB(tabelaFiltrada,tempoValido)

    pcExcesso=calculaPercentualExcessoCorrigido(tabelaFiltrada)

    col1, col2, col3, col4= st.columns(4)

    with col1:
        st.metric("Frequência de uso do celular (usos/hora)",freqUsoCelular)
    with col2:
        st.metric("Percentual do tempo de não uso do cinto de segurança",str(percentWsb)+"%")
    with col3:
        st.metric("Percentual do tempo sob excesso de velocidade*",str(pcExcesso)+"%")
    with col4:
        st.metric("Tempo de viagem (h)",round((tempoValido/3600),2))

    #---------------------------------------------
    separaConteudo()
    # Coloração e inserção do mapa inferior assim como as opções de visualização disponível
    
    options=["Frequência de uso do celular (usos/hora)",
             "Percentual do tempo de não uso do cinto de segurança",
             "Percentual do tempo sob excesso de velocidade*"]

    st.session_state["ESCOLHA"] = st.selectbox("Selecione o parâmetro para ser preenchido o mapa:",
                                               options, 
                                               index=options.index(st.session_state["ESCOLHA"]))

    coloreMapa(st.session_state["ESCOLHA"],tabelaFiltrada,my_map)
    insereMapa(st.session_state["ESCOLHA"],my_map)

    #---------------------------------------------
    separaConteudo()
    ## Rodapé da página

    rodape()

    ##---------------------------------------------

if __name__ == "__main__":
    main()