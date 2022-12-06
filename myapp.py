import streamlit as st
import folium
import re
import pandas as pd
from streamlit_folium import folium_static

st.sidebar.header("user input parameters")
info=st.sidebar.selectbox('viagem',('Primeira','Segunda'))




my_map = folium.Map(location=[-25.436085,-49.269290],zoom_start=13)


if(info=='Primeira'):
    arquivo = open('Dados20220921-190631.csv', 'r')
if(info=='Segunda'):
    arquivo = open('Fulltable_20220429_EFGHSTUV.csv', 'r')

total = arquivo.readlines()


ignoraPrimeira = 0

for linhaAtual in total:
    if (ignoraPrimeira == 0):
        ignoraPrimeira += 1
    else:
        linha = re.split('[,;]',linhaAtual)
        data=linha[5]
        data = data.split('/')
        if(len(data)>1 and float(data[2])==2021):
            longitude = linha[1] + '.' + linha[2]
            longitude = float(longitude)
            latitude = linha[3] + '.'  + linha[4]
            latitude = float(latitude)
        else:
            longitude=float(linha[1])
            latitude=float(linha[2])
            
        folium.Circle([latitude,longitude],5,color='black',fill=True,fill_color='black',fill_opacity=1).add_to(my_map)


folium_static(my_map,width=800,height=475)
