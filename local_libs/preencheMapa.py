# Autor: Leonardo Becker de Oliveira
# Contato: leonardobecker79@gmail.com
# Link para o repositório: https://github.com/LeonardooBecker/streamlit

import pandas as pd
from calculaParametros import *
from branca.colormap import linear
from streamlit_folium import folium_static
import folium
import streamlit as st


# Preenche o mapa com os dados e cores de acordo com a escolha do usuário
def coloreMapa(escolha, tabela, my_map):
    allBairros = pd.Series.unique(tabela["BAIRRO"])
    allBairros = allBairros.tolist()

    arq = open('./data/data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")
    dfCodigo = pd.read_csv('./data/codigoBairros.csv', sep=',')

    maxValue = 0
    for i in allBairros:
        if (i != "NPI"):

            df = tabela[tabela["BAIRRO"] == i]
            tempoValido=calculaTempoValido(df)

            linedf = dfCodigo[dfCodigo["BAIRRO"] == i]
            codigo = int(linedf["CODIGO"].iloc[0])

            if (escolha == "Frequência de uso do celular (usos/hora)"):
                freqUso=calculaFreqUsoCelular(df,tempoValido)*1000
                line = str(i)+","+str(codigo)+","+str(int(freqUso))+"\n"
                arq.write(line)

                #Escala de cores buscando definida sempre pelo maior valor
                if (freqUso > maxValue):
                    maxValue = freqUso
                colormap = linear.YlOrRd_09.scale(0, maxValue/1000)
                colormap.caption = "Frequência de uso do celular por hora"

            if (escolha == "Percentual do tempo de não uso do cinto de segurança"):
                percentWsb=calculaPercentWSB(df,tempoValido)*100
                line = str(i)+','+str(codigo)+','+str(int(percentWsb))+'\n'
                arq.write(line)
                
                #Escala de cores buscando definida sempre pelo maior valor
                if (percentWsb > maxValue):
                    maxValue = percentWsb
                colormap = linear.YlOrRd_09.scale(0, maxValue/100)
                colormap.caption = "Percentual do tempo sem o uso do cinto de segurança"


            if (escolha == "Percentual do tempo sob excesso de velocidade*"):
                pcExcesso=calculaPercentualExcesso(df)*100
                line = str(i)+','+str(codigo)+','+str(int(pcExcesso))+'\n'
                arq.write(line)
                
                #Escala de cores buscando definida sempre pelo maior valor
                if (pcExcesso > maxValue):
                    maxValue = pcExcesso
                colormap = linear.YlOrRd_09.scale(0, maxValue/100)
                colormap.caption = "Percentual do tempo sob excesso de velocidade"

    arq.close()

    colormap.add_to(my_map)

    state_data = pd.read_csv('./data/data.csv', encoding='latin-1')

    choropleth = folium.Choropleth(
        geo_data='./data/bairros.geo.json',
        data=state_data,
        columns=['Codigo', 'Pinta'],
        key_on='feature.properties.codigo',
        fill_color="YlOrRd",
        fill_opacity=0.5,
        nan_fill_opacity=0,
        line_color="Gray",
        line_opacity=0.4
    )
    choropleth.geojson.add_to(my_map)

    state_data_indexed = state_data.set_index('Codigo')

    for s in choropleth.geojson.data['features']:
        if ((s['properties']['codigo']) in state_data['Codigo'].values):
            valor = s['properties']['codigo']
            if (escolha == "Frequência de uso do celular (usos/hora)"):
                s['properties']['valor'] = int(
                    state_data_indexed.loc[valor, "Pinta"])/1000
            else:
                s['properties']['valor'] = int(
                    state_data_indexed.loc[valor, "Pinta"])/100
        else:
            s['properties']['valor'] = 0

    folium.GeoJsonTooltip(['nome', 'valor']).add_to(choropleth.geojson)

# Insere o mapa e sua respectiva leganda na página
def insereMapa(escolha,my_map):
    if(escolha=="Frequência de uso do celular (usos/hora)"):
        st.subheader("Mapa de calor representando a frequência de uso do celular por hora")

    if(escolha=="Percentual do tempo de não uso do cinto de segurança"):
        st.subheader("Mapa de calor representando o percentual do tempo sem o uso do cinto de segurança")

    if(escolha=="Percentual do tempo sob excesso de velocidade*"):
        st.subheader("Mapa de calor representando o percentual do tempo sob o excesso de velocidade")

    folium_static(my_map)