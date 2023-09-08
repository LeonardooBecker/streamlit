# Autor: Leonardo Becker de Oliveira
# Contato: leonardobecker79@gmail.com
# Link para o repositório: https://github.com/LeonardooBecker/streamlit

import pandas as pd
from calculaParametros import *
from branca.colormap import linear
from streamlit_folium import folium_static
import folium
import streamlit as st


# Preenche no arquivo a frequencia de uso do celular por hora de acordo com o bairro e seu respectivo codigo
def OptFrequenciaCelular(arq, bairro, codigo, df, maxValue):
    tempoValido = calculaTempoValido(df)
    freqUso = calculaFreqUsoCelular(df, tempoValido)*1000
    arq.write(str(bairro)+","+str(codigo)+","+str(int(freqUso))+"\n")
    if (freqUso > maxValue):
        maxValue = freqUso
    colormap = linear.YlOrRd_09.scale(0, maxValue/1000)
    colormap.caption = "Frequência de uso do celular por hora"
    return colormap, maxValue

# Preenche no arquivo o percentual de tempo sem o uso do cinto de segurança de acordo com o bairro e seu respectivo codigo
def OptPercentWSB(arq, bairro, codigo, df, maxValue):
    tempoValido = calculaTempoValido(df)
    percentWsb = calculaPercentWSB(df, tempoValido)*100
    arq.write(str(bairro)+","+str(codigo)+","+str(int(percentWsb))+"\n")
    if (percentWsb > maxValue):
        maxValue = percentWsb
    colormap = linear.YlOrRd_09.scale(0, maxValue/100)
    colormap.caption = "Percentual do tempo de não uso do cinto de segurança"
    return colormap, maxValue

# Preenche no arquivo o percentual de tempo sob excesso de velocidade de acordo com o bairro e seu respectivo codigo
def OptPercentualVelocidade(arq, bairro, codigo, df, maxValue):
    pcExcesso = calculaPercentualExcessoCorrigido(df)*100
    arq.write(str(bairro)+","+str(codigo)+","+str(int(pcExcesso))+"\n")
    if (pcExcesso > maxValue):
        maxValue = pcExcesso
    colormap = linear.YlOrRd_09.scale(0, maxValue/100)
    colormap.caption = "Percentual do tempo sob excesso de velocidade*"
    return colormap, maxValue

# Preenche no arquivo o percentual de tempo usando o celular de acordo com o bairro e seu respectivo codigo
def OptPercentualCelular(arq, bairro, codigo, df, maxValue):
    tempoValido = calculaTempoValido(df)
    percentUso = calculaPercentualUsoCelular(df, tempoValido)*100
    arq.write(str(bairro)+","+str(codigo)+","+str(int(percentUso))+"\n")
    if (percentUso > maxValue):
        maxValue = percentUso
    colormap = linear.YlOrRd_09.scale(0, maxValue/100)
    colormap.caption = "Percentual do tempo de uso do celular"
    return colormap, maxValue

def OptPercentualCinto(arq,bairro,codigo,df,maxValue,escolhaLimite):
    dfVelocidade=df["SPD_KMH"]
    dfLimite=df["LIMITE_VEL"]
    if(escolhaLimite=="Acima do limite"):
        df=df[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    elif (escolhaLimite=="Abaixo do limite"):
        df=df[(dfVelocidade<=dfLimite) & (dfLimite!=0)]
    tempoValido=calculaTempoValido(df)
    percentWsb=calculaPercentWSB(df,tempoValido)*100
    line=str(bairro)+','+str(codigo)+','+str(int(percentWsb))+'\n'
    arq.write(line)
    
    if(percentWsb>maxValue):
        maxValue=percentWsb
    colormap = linear.YlOrRd_09.scale(0, maxValue/100)
    colormap.caption = "Percentual do tempo de uso do celular"
    return colormap, maxValue
                    



# Preenche o mapa com os dados e cores de acordo com a escolha do usuário
def coloreMapa(escolha, tabela, my_map):
    allBairros = pd.Series.unique(tabela["BAIRRO"])
    allBairros = allBairros.tolist()

    arq = open('./data/data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")
    dfCodigo = pd.read_csv('./data/codigoBairros.csv', sep=',')

    maxValue = 0

    for bairro in allBairros:
        if (bairro != "NPI"):

            df = tabela[tabela["BAIRRO"] == bairro]
            tempoValido = calculaTempoValido(df)

            linedf = dfCodigo[dfCodigo["BAIRRO"] == bairro]
            codigo = int(linedf["CODIGO"].iloc[0])

            if (escolha == "Frequência de uso do celular (usos/hora)"):
                colormap, maxValue = OptFrequenciaCelular(arq, bairro, codigo, df, maxValue)

            if (escolha == "Percentual do tempo de não uso do cinto de segurança"):
                colormap, maxValue = OptPercentWSB(arq, bairro, codigo, df, maxValue)

            if (escolha == "Percentual do tempo sob excesso de velocidade*"):
                colormap, maxValue = OptPercentualVelocidade(arq, bairro, codigo, df, maxValue)

            if (escolha == "Percentual do uso de celular"):
                colormap, maxValue = OptPercentualCelular(arq, bairro, codigo, df, maxValue)

            if (escolha=="Independente do limite" or escolha=="Acima do limite" or escolha=="Abaixo do limite"):
                colormap, maxValue = OptPercentualCinto(arq,bairro,codigo,df,maxValue,escolha)

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
def insereMapa(escolha, my_map):
    if (escolha == "Frequência de uso do celular (usos/hora)"):
        st.subheader("Mapa de calor representando a frequência de uso do celular por hora")

    if (escolha == "Percentual do tempo de não uso do cinto de segurança"):
        st.subheader("Mapa de calor representando o percentual do tempo sem o uso do cinto de segurança")

    if (escolha == "Percentual do tempo sob excesso de velocidade*"):
        st.subheader("Mapa de calor representando o percentual do tempo sob o excesso de velocidade*")
        
    if (escolha == "Percentual do uso de celular"):
        st.subheader("Percentual do tempo de viagem usando o celular segundo bairro de Curitiba (usos/h)")

    folium_static(my_map)
