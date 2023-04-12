import streamlit as st
import folium
import pandas as pd
import random
import time
import os
from streamlit_folium import folium_static


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
        vetor.sort()


def atualizaInfo(total, dadosIndice):
    vet = []
    # Cria vetores auxiliares para poder atualizar os filtros
    novoCondutores = []
    novohCwb = []
    novohCtb = []
    novoBairro = []
    novoCidade = []
    novoViagem = []

    if (dadosIndice[0][0] == ""):
        novoCondutores.append("")
    if (dadosIndice[1][0] == ""):
        novohCwb.append("")
    if (dadosIndice[2][0] == ""):
        novohCtb.append("")
    if (dadosIndice[3][0] == ""):
        novoBairro.append("")
    if (dadosIndice[4][0] == ""):
        novoCidade.append("")
    if (dadosIndice[5][0] == ""):
        novoViagem.append("")

    for linhaAtual in total:
        linha = linhaAtual.split(';')
        adicionaValor = 1

        for i in dadosIndice:
            if (i[0] != ""):
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



def pintaBairro(bairroSelec):
    #Escreve a primeira linha, padrao para qualquer tipo de bairro ( inclusive o NULL )
    arq=open('data.csv','w')
    arq.write("Bairros,Codigo,Pinta\n")

    # Caso algum bairro venha a ser selecionado, escreve o seu nome e codigo na linha subjacente
    if(bairroSelec!=""):
        arqCodigo=open('codigoBairros.csv','r')

        full=arqCodigo.readlines()
        
        #Laço de repetição que busca pelo nome o codigo do bairro
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

total=[]
for file in os.listdir("./"):
    if file.startswith("Fulltable") and file.endswith(".csv"):
        arquivo=open(file,'r')
        total.extend((arquivo.readlines()))
        arquivo.close()


st.sidebar.header("user input parameters")

my_map = folium.Map(location=[-25.436085, -49.269290], zoom_start=13, tiles='CartoDB positron')

# arquivo = open('FullTables/Fulltable_20220429_EFGHSTUV.csv', 'r')
# total = arquivo.readlines()



condutores = [""]
hCtb = [""]
hCwb = [""]
bairro = [""]
cidade = [""]
viagem = [""]

st.session_state[0]=''

# Cria vetores contendo as informaçoes da sidebar
for linhaAtual in total:
    linha = linhaAtual.split(';')
    adicionaInfo(condutores, 0, linha, "DRIVER")
    adicionaInfo(hCtb, 32, linha, "HIERARQUIA_CTB")
    adicionaInfo(hCwb, 31, linha, "HIERARQUIA_CWB")
    adicionaInfo(cidade, 28, linha, "CIDADE")
    adicionaInfo(bairro, 29, linha, "BAIRRO")
    adicionaInfo(viagem, 7, linha, "ID")

# Primeiro caso, ontem a pagina foi recem aberta/recarregada, e todos os filtros estão em NULL
if 1 not in st.session_state:
    condut = st.sidebar.selectbox('DRIVER', condutores)
    hCwbSelec = st.sidebar.selectbox('HIERARQUIA_CWB', hCwb)
    hCtbSelec = st.sidebar.selectbox('HIERARQUIA_CTB', hCtb)
    bairroSelec = st.sidebar.selectbox('BAIRRO', bairro)
    cidadeSelec = st.sidebar.selectbox('CIDADE', cidade)
    viagemSelec = st.sidebar.selectbox('ID', viagem)

# Caso contrário atualiza de acordo com os filtros selecionados
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

# Copia os estados do filtro para o vetor dadosIndice
dadosIndice = []
dadosIndice.append([condut, 0])
dadosIndice.append([hCwbSelec, 31])
dadosIndice.append([hCtbSelec, 32])
dadosIndice.append([bairroSelec, 29])
dadosIndice.append([cidadeSelec, 28])
dadosIndice.append([viagemSelec, 7])

# E então atualiza de acordo com os selecionados, por exemplo, caso tenha sido selecionado
# o DRIVER X, so aparece os bairros ( e outros filtros ) que o DRIVER X passou em alguma das suas viagens
atualizaInfo(total, dadosIndice)


# Aplica os filtros para ficar tudo de acordo conforme estabelecido em atualizaInfo()
if(st.session_state[1]!=condutores):
    st.experimental_rerun()
if(st.session_state[2]!=hCwb):
    st.experimental_rerun()
if(st.session_state[3]!=hCtb):
    st.experimental_rerun()
if(st.session_state[4]!=bairro):
    st.experimental_rerun()
if(st.session_state[5]!=cidade):
    st.experimental_rerun()
if(st.session_state[6]!=viagem):
    st.experimental_rerun()

# Pinta a região no mapa de acordo com o bairro selecionado
pintaBairro(bairroSelec)


if st.sidebar.button('Refresh Page'):
    st.session_state.clear()
    st.experimental_rerun()


ignoraPrimeira = 0
count = 0
for linhaAtual in total:
    linha = linhaAtual.split(';')
    if (ignoraPrimeira == 0):
        ignoraPrimeira += 1
    else:
        if (((linha[0] == condut) or (condut == "")) and ((linha[32] == hCtbSelec) or (hCtbSelec == "")) and ((linha[31] == hCwbSelec) or (hCwbSelec == "")) and ((linha[28] == cidadeSelec) or (cidadeSelec == "")) and ((linha[29] == bairroSelec) or (bairroSelec == "")) and ((linha[7] == viagemSelec) or (viagemSelec == "")) and ((condut != "") or (hCtbSelec != "") or (hCwbSelec != "") or (cidadeSelec != "") or (bairroSelec != "") or (viagemSelec != ""))):
            count += 1
            linha[1] = linha[1].replace(',', '.')
            linha[2] = linha[2].replace(',', '.')
            if(linha[1]==''):
                linha[1]=0
            if(linha[2]==''):
                linha[2]=0
            longitude = float(linha[1])
            latitude = float(linha[2])
            # x=random.randint(1,100)
            # if(x>90):
            #     folium.Circle([latitude, longitude], 3,
            #               color='black').add_to(my_map)

st.write(count)
folium_static(my_map, width=800, height=475)