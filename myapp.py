import streamlit as st
import folium
import pandas as pd
import random
import time
from streamlit_folium import folium_static
maxMessageSize = 1000


def adicionaInfo(vetor, indice, linhaAtual, infoAtual):
    adicionaValor = 1
    # Para cada elemento do vetor verifica se o elemento da linhaAtual ja esta presente no vetor
    for i in vetor:
        if (linhaAtual[indice] == i):
            adicionaValor = 0
    # Elimina o elemento que contem o nome da informação que esta trabalhando
    if (linhaAtual[indice] == infoAtual):
        adicionaValor = 0
    # Caso as duas condições acimas estejam de acordo insere no vetor
    if (adicionaValor == 1):
        vetor.append(linhaAtual[indice])


st.sidebar.header("user input parameters")
# info=st.sidebar.selectbox('viagem',('Primeira','Segunda'))

my_map = folium.Map(location=[-25.436085, -49.269290], zoom_start=13, tiles='CartoDB positron')

# if(info=='Primeira'):
#     arquivo = open('Dados20220921-190631.csv', 'r')
# if(info=='Segunda'):
#     arquivo = open('Fulltable_20220429_EFGHSTUV.csv', 'r')
arquivo = open('Fulltable_20220429_EFGHSTUV.csv', 'r')
total = arquivo.readlines()

driverAnterior = 'DRIVER'

condutores = ["NULL"]
hCtb = ["NULL"]
hCwb = ["NULL"]
bairro = ["NULL"]
cidade = ["NULL"]
viagem = ["NULL"]


# Cria vetores contendo as informaçoes da sidebar
for linhaAtual in total:
    linha = linhaAtual.split(';')
    adicionaInfo(condutores, 0, linha, "DRIVER")
    adicionaInfo(hCtb, 32, linha, "HIERARQUIA_CTB")
    adicionaInfo(hCwb, 31, linha, "HIERARQUIA_CWB")
    adicionaInfo(cidade, 28, linha, "CIDADE")
    adicionaInfo(bairro, 29, linha, "BAIRRO")
    adicionaInfo(viagem, 7, linha, "ID")


st.session_state[0] = ''


if 1 not in st.session_state:
    condut = st.sidebar.selectbox('DRIVER', condutores)
    hCwbSelec = st.sidebar.selectbox('HIERARQUIA_CWB', hCwb)
    hCtbSelec = st.sidebar.selectbox('HIERARQUIA_CTB', hCtb)
    bairroSelec = st.sidebar.selectbox('BAIRRO', bairro)
    cidadeSelec = st.sidebar.selectbox('CIDADE', cidade)
    viagemSelec = st.sidebar.selectbox('ID', viagem)


else:
    condutores = st.session_state[1]
    condut = st.sidebar.selectbox('DRIVER', condutores)
    hCwb = st.session_state[2]
    hCwbSelec = st.sidebar.selectbox('HIERARQUIA_CWB', hCwb)
    hCtb = st.session_state[3]
    hCtbSelec = st.sidebar.selectbox('HIERARQUIA_CTB', hCtb)
    bairro = st.session_state[4]
    bairroSelec = st.sidebar.selectbox('BAIRRO', bairro)
    cidade = st.session_state[5]
    cidadeSelec = st.sidebar.selectbox('CIDADE', cidade)
    viagem = st.session_state[6]
    viagemSelec = st.sidebar.selectbox('ID', viagem)

dadosIndice = []
dadosIndice.append([condut, 0])
dadosIndice.append([hCwbSelec, 31])
dadosIndice.append([hCtbSelec, 32])
dadosIndice.append([bairroSelec, 29])
dadosIndice.append([cidadeSelec, 28])
dadosIndice.append([viagemSelec, 7])

def atualizaInfo(total, dadosIndice):
    vet = []
    novoCondutores = []
    novohCwb = []
    novohCtb = []
    novoBairro = []
    novoCidade = []
    novoViagem = []

    if (dadosIndice[0][0] == "NULL"):
        novoCondutores.append("NULL")
    if (dadosIndice[1][0] == "NULL"):
        novohCwb.append("NULL")
    if (dadosIndice[2][0] == "NULL"):
        novohCtb.append("NULL")
    if (dadosIndice[3][0] == "NULL"):
        novoBairro.append("NULL")
    if (dadosIndice[4][0] == "NULL"):
        novoCidade.append("NULL")
    if (dadosIndice[5][0] == "NULL"):
        novoViagem.append("NULL")

    for linhaAtual in total:
        linha = linhaAtual.split(';')
        adicionaValor = 1

        for i in dadosIndice:
            if (i[0] != "NULL"):
                if (linha[(i[1])] != i[0]):
                    adicionaValor = 0
        if (adicionaValor == 1):
            vet.append(linhaAtual)
    for linhaAtual in vet:
        linha = linhaAtual.split(';')
        adicionaInfo(novoCondutores, 0, linha, "DRIVER")
        adicionaInfo(novohCtb, 32, linha, "HIERARQUIA_CTB")
        adicionaInfo(novohCwb, 31, linha, "HIERARQUIA_CWB")
        adicionaInfo(novoCidade, 28, linha, "CIDADE")
        adicionaInfo(novoBairro, 29, linha, "BAIRRO")
        adicionaInfo(novoViagem, 7, linha, "ID")

    st.session_state[1] = novoCondutores
    st.session_state[2] = novohCwb
    st.session_state[3] = novohCtb
    st.session_state[4] = novoBairro
    st.session_state[5] = novoCidade
    st.session_state[6] = novoViagem

if(bairroSelec=="NULL"):
    arq=open('data.csv','w')
    arq.write("Bairros,Codigo,Pinta\n")
    arq.close()
else:
    arq=open('data.csv','w')
    arq.write("Bairros,Codigo,Pinta\n")
    arqCodigo=open('codigoBairros.csv','r');
    full=arqCodigo.readlines()
    for i in full:
        sep = i.split(',')
        if(sep[0]==bairroSelec):            
            arq.write(sep[0]+','+sep[1].rstrip("\n")+','+"1")
    arq.close()

state_data=pd.read_csv('data.csv',encoding='latin-1')

choropleth = folium.Choropleth(
    geo_data='bairros.geo.json',
    data=state_data,
    columns=['Codigo','Pinta'],
    key_on='feature.properties.codigo',
    fill_color="YlOrRd",
    fill_opacity=0.5,
    nan_fill_opacity=0,
    line_opacity=0
)
choropleth.geojson.add_to(my_map)

arq=open('data.csv','w')
arq.write("Bairros,Codigo,Pinta\n")
arq.write("XAXIM,57,1")
arq.close()

atualizaInfo(total, dadosIndice)


# st.session_state

if st.sidebar.button('Apply Filter'):
    st.experimental_rerun()

if st.sidebar.button('Refresh Page'):
    st.session_state.clear();
    st.experimental_rerun()

ignoraPrimeira = 0
count = 0
for linhaAtual in total:
    linha = linhaAtual.split(';')
    if (ignoraPrimeira == 0):
        ignoraPrimeira += 1
    else:
        if (((linha[0] == condut) or (condut == "NULL")) and ((linha[32] == hCtbSelec) or (hCtbSelec == "NULL")) and ((linha[31] == hCwbSelec) or (hCwbSelec == "NULL")) and ((linha[28] == cidadeSelec) or (cidadeSelec == "NULL")) and ((linha[29] == bairroSelec) or (bairroSelec == "NULL")) and ((linha[7] == viagemSelec) or (viagemSelec == "NULL")) and ((condut != "NULL") or (hCtbSelec != "NULL") or (hCwbSelec != "NULL") or (cidadeSelec != "NULL") or (bairroSelec != "NULL") or (viagemSelec != "NULL"))):
            count += 1
            linha[1] = linha[1].replace(',', '.')
            linha[2] = linha[2].replace(',', '.')
            longitude = float(linha[1])
            latitude = float(linha[2])
            # folium.Circle([latitude,longitude],5,color='black',fill=True,fill_color='black',fill_opacity=1).add_to(my_map)
            x=random.randint(1,100)
            if(x>50):
                folium.Circle([latitude, longitude], 3,
                          color='black').add_to(my_map)

st.write(count)
folium_static(my_map, width=800, height=475)
