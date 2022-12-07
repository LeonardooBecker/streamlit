import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

def adicionaInfo(vetor,indice,linhaAtual,infoAtual):
    adicionaValor=1
    # Para cada elemento do vetor verifica se o elemento da linhaAtual ja esta presente no vetor
    for i in vetor:
        if(linhaAtual[indice]==i):
            adicionaValor=0
    # Elimina o elemento que contem o nome da informação que esta trabalhando
    if(linhaAtual[indice]==infoAtual):
        adicionaValor=0
    # Caso as duas condições acimas estejam de acordo insere no vetor
    if(adicionaValor==1):
        vetor.append(linhaAtual[indice])


st.sidebar.header("user input parameters")
info=st.sidebar.selectbox('viagem',('Primeira','Segunda'))

my_map = folium.Map(location=[-25.436085,-49.269290],zoom_start=13)


if(info=='Primeira'):
    arquivo = open('Dados20220921-190631.csv', 'r')
if(info=='Segunda'):
    arquivo = open('Fulltable_20220429_EFGHSTUV.csv', 'r')
total = arquivo.readlines()

driverAnterior='DRIVER'

condutores = []
hCtb = []
hCwb = []
bairro = []
cidade = []
viagem = []


#Cria vetores contendo as informaçoes da sidebar
for linhaAtual in total:
    linha=linhaAtual.split(';')
    adicionaInfo(condutores,0,linha,"DRIVER")
    adicionaInfo(hCtb,32,linha,"HIERARQUIA_CTB")
    adicionaInfo(hCwb,31,linha,"HIERARQUIA_CWB")
    adicionaInfo(cidade,28,linha,"CIDADE")
    adicionaInfo(bairro,29,linha,"BAIRRO")
    adicionaInfo(viagem,7,linha,"ID")
        

condut=st.sidebar.selectbox('condutor',condutores)
hCwbSelec=st.sidebar.selectbox('HIERARQUIA_CWB',hCwb)
hCtbSelec=st.sidebar.selectbox('HIERARQUIA_CTB',hCtb)
bairroSelec=st.sidebar.selectbox('BAIRRO',bairro)
cidadeSelec=st.sidebar.selectbox('CIDADE',cidade)
viagemSelec=st.sidebar.selectbox('ID',viagem)

ignoraPrimeira = 0

for linhaAtual in total:
    linha=linhaAtual.split(';')
    if (ignoraPrimeira == 0):
        ignoraPrimeira += 1
    else:
        if(linha[0]==condut and linha[32]==hCtbSelec):
            linha[1]=linha[1].replace(',','.')
            linha[2]=linha[2].replace(',','.')
            longitude=float(linha[1])
            latitude=float(linha[2])
            #folium.Circle([latitude,longitude],5,color='black',fill=True,fill_color='black',fill_opacity=1).add_to(my_map)
            folium.Circle([latitude,longitude],5,color='black').add_to(my_map)


folium_static(my_map,width=800,height=475)
