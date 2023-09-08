import pandas as pd
from branca.colormap import linear
from streamlit_folium import folium_static
import folium
import streamlit as st


def insereMapaRadar(map_radar):
    radares = pd.read_csv("./data/radares.csv", sep=",")

    # Para cada linha presente no csv, adiciona um marcador no mapa
    for i, j in radares.iterrows():

        # Se for do tipo Lombada, adiciona um marcador azul
        if 'LOMBADA' in j['Tipo']:
            longitude = float(j['Longitude'])
            latitude = float(j['Latitude'])
            folium.Circle([latitude, longitude], 15,
                        color='blue', fill_color="blue", fill_opacity=0.7).add_to(map_radar)
            
        # Se for do tipo Radar, adiciona um marcador vermelho
        elif 'RADAR' in j['Tipo']:
            longitude = float(j['Longitude'])
            latitude = float(j['Latitude'])
            folium.Circle([latitude, longitude], 15,
                        color='red', fill_color="red", fill_opacity=0.7).add_to(map_radar)

    st.subheader("Localização dos dispositivos de fiscalização eletrônica de velocidade")

    col1, col2 = st.columns(2)
    with col1:
        texto_html = f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:red;margin-right:5px;"></span>RADAR - CONSILUX'
        st.markdown(texto_html, unsafe_allow_html=True)
    with col2:
        texto_html = f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:blue;margin-right:5px;"></span>LOMBADA - CONSILUX'
        st.markdown(texto_html, unsafe_allow_html=True)

    folium_static(map_radar)