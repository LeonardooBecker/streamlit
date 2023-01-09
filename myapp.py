import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium


def pintaBairro(bairroSelec):
    # Escreve a primeira linha, padrao para qualquer tipo de bairro ( inclusive o NULL )
    arq = open('data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")

    # Caso algum bairro venha a ser selecionado, escreve o seu nome e codigo na linha subjacente
    if (bairroSelec != ""):
        arqCodigo = open('codigoBairros.csv', 'r')

        full = arqCodigo.readlines()

        # Laço de repetição que busca pelo nome o codigo do bairro
        for i in full:
            sep = i.split(',')
            if (sep[0] == bairroSelec):
                arq.write(sep[0]+','+sep[1].rstrip("\n")+','+"1")

    arq.close()

    state_data = pd.read_csv('data.csv', encoding='latin-1')

    choropleth = folium.Choropleth(
        geo_data='bairros.geo.json',
        data=state_data,
        columns=['Codigo', 'Pinta'],
        key_on='feature.properties.codigo',
        fill_color="YlOrRd",
        fill_opacity=0.5,
        nan_fill_opacity=0,
        line_opacity=0
    )
    choropleth.geojson.add_to(my_map)


def atualizaInfo(tabela, param):
    drivers = (pd.Series.unique(tabela["DRIVER"])).astype(str)
    drivers = drivers.tolist()
    if (param[0][1] == ""):
        drivers.append("")
    drivers.sort()
    idades = (pd.Series.unique(tabela["IDADE"])).astype(str)
    idades = idades.tolist()
    if (param[3][1] == ""):
        idades.append("")
    idades.sort()
    bairros = (pd.Series.unique(tabela["BAIRRO"])).astype(str)
    bairros = bairros.tolist()
    if (param[1][1] == ""):
        bairros.append("")
    bairros.sort()
    cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str)
    cidades = cidades.tolist()
    if (param[2][1] == ""):
        cidades.append("")
    cidades.sort()
    hCtb = (pd.Series.unique(tabela["HIERARQUIA_CTB"])).astype(str)
    hCtb = hCtb.tolist()
    if (param[5][1] == ""):
        hCtb.append("")
    hCtb.sort()
    hCwb = (pd.Series.unique(tabela["HIERARQUIA_CWB"])).astype(str)
    hCwb = hCwb.tolist()
    if (param[4][1] == ""):
        hCwb.append("")
    hCwb.sort()
    ids = (pd.Series.unique(tabela["ID"])).astype(str)
    ids = ids.tolist()
    if (param[6][1] == ""):
        ids.append("")
    ids.sort()

    st.session_state[1] = drivers
    st.session_state[2] = hCwb
    st.session_state[3] = hCtb
    st.session_state[4] = bairros
    st.session_state[5] = cidades
    st.session_state[6] = ids
    st.session_state[7] = idades


my_map = folium.Map(location=[-25.436085, -49.269290],
                    zoom_start=13, tiles='CartoDB positron')

tabela = pd.read_csv("AllFullTable.csv", sep=";", low_memory=False)

drivers = (pd.Series.unique(tabela["DRIVER"])).astype(str)
drivers = drivers.tolist()
drivers.append("")
drivers.sort()
idades = (pd.Series.unique(tabela["IDADE"])).astype(str)
idades = idades.tolist()
idades.append("")
idades.sort()
bairros = (pd.Series.unique(tabela["BAIRRO"])).astype(str)
bairros = bairros.tolist()
bairros.append("")
bairros.sort()
cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str)
cidades = cidades.tolist()
cidades.append("")
cidades.sort()
hCtb = (pd.Series.unique(tabela["HIERARQUIA_CTB"])).astype(str)
hCtb = hCtb.tolist()
hCtb.append("")
hCtb.sort()
hCwb = (pd.Series.unique(tabela["HIERARQUIA_CWB"])).astype(str)
hCwb = hCwb.tolist()
hCwb.append("")
hCwb.sort()
ids = (pd.Series.unique(tabela["ID"])).astype(str)
ids = ids.tolist()
ids.append("")
ids.sort()


if 1 not in st.session_state:
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    hCwbSelec = st.sidebar.selectbox('Hierarquia viária (Curitiba)', hCwb)
    hCtbSelec = st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb)
    bairroSelec = st.sidebar.selectbox('Bairro', bairros)
    cidadeSelec = st.sidebar.selectbox('Cidade', cidades)
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    idSelec = st.sidebar.selectbox('Viagem', ids)

else:
    idades=st.session_state[7]
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    hCwb=st.session_state[2]
    hCwbSelec = st.sidebar.selectbox('Hierarquia viária (Curitiba)', hCwb)
    hCtb=st.session_state[3]
    hCtbSelec = st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb)
    bairros=st.session_state[4]
    bairroSelec = st.sidebar.selectbox('Bairro', bairros)
    cidades=st.session_state[5]
    cidadeSelec = st.sidebar.selectbox('Cidade', cidades)
    drivers=st.session_state[1]
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    ids=st.session_state[6]
    idSelec = st.sidebar.selectbox('Viagem', ids)

param = []
param.append([0, driverSelec])
param.append([1, bairroSelec])
param.append([2, cidadeSelec])
param.append([3, idadeSelec])
param.append([4, hCwbSelec])
param.append([5, hCtbSelec])
param.append([6, idSelec])

resul = tabela

for i in param:
    if (i[0] == 0 and (i[1] != "")):
        resul = resul[resul["DRIVER"] == i[1]]
    if (i[0] == 1 and (i[1] != "")):
        resul = resul[resul["BAIRRO"] == i[1]]
    if (i[0] == 2 and (i[1] != "")):
        resul = resul[resul["CIDADE"] == i[1]]
    if (i[0] == 3 and (i[1] != "")):
        resul = resul[resul["IDADE"] == i[1]]
    if (i[0] == 4 and (i[1] != "")):
        resul = resul[resul["HIERARQUIA_CWB"] == i[1]]
    if (i[0] == 5 and (i[1] != "")):
        resul = resul[resul["HIERARQUIA_CTB"] == i[1]]
    if (i[0] == 6 and (i[1] != "")):
        resul = resul[resul["ID"] == i[1]]

atualizaInfo(resul,param)

if(st.session_state[1]!=drivers):
    st.experimental_rerun()
if(st.session_state[2]!=hCwb):
    st.experimental_rerun()
if(st.session_state[3]!=hCtb):
    st.experimental_rerun()
if(st.session_state[4]!=bairros):
    st.experimental_rerun()
if(st.session_state[5]!=cidades):
    st.experimental_rerun()
if(st.session_state[6]!=ids):
    st.experimental_rerun()
if(st.session_state[7]!=idades):
    st.experimental_rerun()


pintaBairro(bairroSelec)

if st.sidebar.button('Refresh Page'):
    st.session_state.clear()
    st.experimental_rerun()

folium_static(my_map, width=800, height=475)