import streamlit as st
import pandas as pd
from streamlit_folium import folium_static

my_map = folium.Map(location=[-25.436085,-49.269290],zoom_start=13)

arquivo = open('Dados20220921-190631.csv', 'r')
total = arquivo.readlines()

init = total[1].split(",")

ignoraPrimeira = 0

for linha in total:
    if (ignoraPrimeira == 0):
        ignoraPrimeira += 1
    else:
        linha = linha.split(",")
        folium.Circle([(float(linha[2])),(float(linha[1]))],5,color='black',fill=True,fill_color='black',fill_opacity=1).add_to(my_map)


folium_static(my_map,width=800,height=475)
