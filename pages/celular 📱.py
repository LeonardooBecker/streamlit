import pandas as pd
import streamlit as st
import plotly.express as px
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
    st.session_state["CATEGORIA"]=[""]
    st.session_state["HIERARQUIA_CTB"] = [""]
    st.session_state["WEEKDAY"]=[""]
    st.session_state["ACTION"]=[""]
    st.session_state["DRIVER"] = [""]
    st.session_state["ID"] = [""]

    st.session_state["IDADESELECT"] = ""
    st.session_state["SEXOSELECT"] = ""
    st.session_state["CATEGORIASELECT"]=""  
    st.session_state["HIERARQUIA_CTBSELECT"] = ""
    st.session_state["WEEKDAYSELECT"]=""
    st.session_state["ACTIONSELECT"]=""
    st.session_state["DRIVERSELECT"] = ""
    st.session_state["IDSELECT"] = ""

    st.session_state["ESCOLHA"] = "Frequência de uso do celular (usos/hora)"
    st.session_state["CELULAR"]=True


my_map = folium.Map(location=[-25.442027, -49.269582],
                        zoom_start=12,tiles='CartoDB positron')

tabela = pd.read_csv("./data/AllFullTable.csv", sep=";", low_memory=False)


# Inicialização dos valores
if "CELULAR" not in st.session_state:
    inicializaValores()


# Dicionario { chave : valor } contendo os parametros de interesse
dicionario={
    "IDADE":st.session_state["IDADESELECT"],
    "SEXO":st.session_state["SEXOSELECT"],
    "CATEGORIA":st.session_state["CATEGORIASELECT"],
    "HIERARQUIA_CTB":st.session_state["HIERARQUIA_CTBSELECT"],
    "WEEKDAY":st.session_state["WEEKDAYSELECT"],
    "ACTION":st.session_state["ACTIONSELECT"],
    "DRIVER":st.session_state["DRIVERSELECT"],
    "ID":st.session_state["IDSELECT"]
    }

preencheVetorFiltro(dicionario,tabela)

# Painel lateral - cada linha corresponde a um filtro possível
for chave in dicionario:
    chaveSelect=chave+"SELECT"
    if(chave=="SEXO" or chave=="CATEGORIA"):
        st.session_state[chaveSelect]=st.sidebar.radio(formataNome(chave),st.session_state[chave])
    elif(chave=="HIERARQUIA_CTB"):
        st.session_state[chaveSelect]=desconverteSing(st.sidebar.selectbox(formataNome(chave),st.session_state[chave]))
    elif(chave=="ACTION"):
        st.session_state[chaveSelect]=tradutorPtEn(st.sidebar.selectbox(formataNome(chave),traduzVetor(st.session_state[chave])))
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


# Título da página

titulo("Estudo Naturalístico de Direção Brasileiro - Indicadores sobre o uso do celular ao volante")

#---------------------------------------------

# Calculo e apresentação dos indicadores na box superior

tabelaFiltrada=atualizaTabela(dicionario,tabela)


tempoValidoTotal=calculaTempoValido(tabelaFiltrada)
velDuranteUso = calculaVelocidadeUsoCelular(tabelaFiltrada)
velSemUso=calculaVelocidadeSemUsoCelular(tabelaFiltrada)
freqUsoCelular=calculaFreqUsoCelular(tabelaFiltrada,tempoValidoTotal)
percentUso=calculaPercentualUsoCelular(tabelaFiltrada,tempoValidoTotal)


col1, col2, col3, col4= st.columns(4)
with col1:
    st.metric("Velocidade média durante o uso (km/h)", velDuranteUso)
with col2:
    st.metric("Velocidade média sem o uso (km/h)", velSemUso)
with col3:
    st.metric("Frequência do uso do celular  (usos/h)", freqUsoCelular)
with col4:
    st.metric(" Percentual do tempo de viagem usando o celular",
              str(percentUso)+"%")
              

#---------------------------------------------


# Gráfico de setores

tiposPossiveis = (pd.Series.unique(tabelaFiltrada["ACTION"])).astype(str).tolist()
slices = []
labels = []

for tipoUso in tiposPossiveis:
    if (tipoUso != "nan"):
        valor = tabelaFiltrada[tabelaFiltrada["ACTION"] == tipoUso]
        valor = valor["ACTION"].count()
        slices.append(valor)
        labels.append(tradutorEnPt(tipoUso))
data = {"Tipo de uso": labels, "Quantidade de uso": slices}
st.subheader("Distribuição dos tipos de uso do celular (% do tempo)")
fig = px.pie(data, values='Quantidade de uso', names='Tipo de uso',height=300)
st.write(fig)

#---------------------------------------------

# Gráfico de barras - Cidades

cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str).tolist()
freqCidades = []
cidadesOfc = []

for cidade in cidades:
    dfCidadeAtual = tabelaFiltrada[tabelaFiltrada["CIDADE"] == cidade]
    qntPickUp = (dfCidadeAtual["PICK_UP"].astype(int)).sum(axis=0)

    tempoAuxiliar = (dfCidadeAtual["VALID_TIME"].astype(int)).sum(axis=0)
    if (qntPickUp > 0):
        cidadesOfc.append(cidade)

        freqCidades.append(qntPickUp/(tempoAuxiliar/3600))

data = {"CIDADE": cidadesOfc, "FREQUENCIA": freqCidades}
new_df = pd.DataFrame(data)
dfCidade = new_df.sort_values(["FREQUENCIA"])

st.subheader("Frequência de uso do celular por cidade (usos/h)")
bars = alt.Chart(dfCidade).mark_bar(width=20).encode(
    x='FREQUENCIA',
    y=alt.Y("CIDADE",sort='-x') 
)
st.altair_chart(bars)

#---------------------------------------------

# Gráfico de barras - Bairros


bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str).tolist()
freqBairros = []
bairrosOfc = []
for i in bairros:
    dfBairroAtual = tabelaFiltrada[tabelaFiltrada["BAIRRO"] == i]
    qntPickUp = (dfBairroAtual["PICK_UP"].astype(int)).sum(axis=0)
    tempoAuxiliar = (dfBairroAtual["VALID_TIME"].astype(int)).sum(axis=0)
    if (qntPickUp > 0):
        bairrosOfc.append(i)
        freqBairros.append(qntPickUp/(tempoAuxiliar/3600))

data = {"BAIRRO": bairrosOfc, "FREQUENCIA": freqBairros}
new_df = pd.DataFrame(data)
dfBairro = new_df.sort_values(["FREQUENCIA"])

st.subheader("Frequência de uso do celular por bairro (usos/h)")
bars = alt.Chart(dfBairro).mark_bar(width=20).encode(
    x='FREQUENCIA',
    y=alt.Y("BAIRRO",sort='-x') 
)
st.altair_chart(bars)

#---------------------------------------------

# Inserção do mapa

coloreMapa("Percentual do uso de celular",tabelaFiltrada,my_map)

insereMapa("Percentual do uso de celular",my_map)

## Rodapé da página

rodape()