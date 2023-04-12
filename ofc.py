import sqlite3
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium

con = sqlite3.connect('meu_banco.db')
cursor = con.cursor()



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


def atualizaInfo(dadosIndice):
    texto = ''

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

    if (dadosIndice[0][0] != ""):
        wd = str(dadosIndice[0][0])
        if (texto == ''):
            texto = texto+'DRIVER='+"'"+wd+"'"
        else:
            texto = texto+' and DRIVER='+"'"+wd+"'"
    if (dadosIndice[1][0] != ""):
        wd = str(dadosIndice[1][0])
        if (texto == ''):
            texto = texto+'HIERARQUIA_CWB='+"'"+wd+"'"
        else:
            texto = texto+' and HIERARQUIA_CWB='+"'"+wd+"'"
    if (dadosIndice[2][0] != ""):
        wd = str(dadosIndice[2][0])
        if (texto == ''):
            texto = texto+'HIERARQUIA_CTB='+"'"+wd+"'"
        else:
            texto = texto+' and HIERARQUIA_CTB='+"'"+wd+"'"
    if (dadosIndice[3][0] != ""):
        wd = str(dadosIndice[3][0])
        if (texto == ''):
            texto = texto+'BAIRRO='+"'"+wd+"'"
        else:
            texto = texto+' and BAIRRO='+"'"+wd+"'"
    if (dadosIndice[4][0] != ""):
        wd = str(dadosIndice[4][0])
        if (texto == ''):
            texto = texto+'CIDADE='+"'"+wd+"'"
        else:
            texto = texto+' and CIDADE='+"'"+wd+"'"
    if (dadosIndice[5][0] != ""):
        wd = str(dadosIndice[5][0])
        if (texto == ''):
            texto = texto+'ID='+"'"+wd+"'"
        else:
            texto = texto+' and ID='+"'"+wd+"'"


    if(texto!=''):
        for i in cursor.execute(f"SELECT DISTINCT DRIVER from dados where {texto} ORDER BY DRIVER"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "DRIVER"):
                novoCondutores.append(cortado[1])
    
        for i in cursor.execute(f"SELECT DISTINCT HIERARQUIA_CTB from dados where {texto} ORDER BY HIERARQUIA_CTB"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "HIERARQUIA_CTB"):
                novohCtb.append(cortado[1])

        for i in cursor.execute(f"SELECT DISTINCT HIERARQUIA_CWB from dados where {texto} ORDER BY HIERARQUIA_CWB"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "HIERARQUIA_CWB"):
                novohCwb.append(cortado[1])

        for i in cursor.execute(f"SELECT DISTINCT BAIRRO from dados where {texto}ORDER BY BAIRRO"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "BAIRRO"):
                novoBairro.append(cortado[1])

        for i in cursor.execute(f"SELECT DISTINCT CIDADE from dados where {texto}ORDER BY CIDADE"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "CIDADE"):
                novoCidade.append(cortado[1])

        for i in cursor.execute(f"SELECT DISTINCT ID from dados where {texto} ORDER BY ID"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "ID"):
                novoViagem.append(cortado[1])
    
    else:
        for i in cursor.execute("SELECT DISTINCT DRIVER from dados ORDER BY DRIVER"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "DRIVER"):
                novoCondutores.append(cortado[1])

        for i in cursor.execute("SELECT DISTINCT HIERARQUIA_CTB from dados ORDER BY HIERARQUIA_CTB"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "HIERARQUIA_CTB"):
                novohCtb.append(cortado[1])

        for i in cursor.execute("SELECT DISTINCT HIERARQUIA_CWB from dados ORDER BY HIERARQUIA_CWB"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "HIERARQUIA_CWB"):
                novohCwb.append(cortado[1])

        for i in cursor.execute("SELECT DISTINCT BAIRRO from dados ORDER BY BAIRRO"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "BAIRRO"):
                novoBairro.append(cortado[1])

        for i in cursor.execute("SELECT DISTINCT CIDADE from dados ORDER BY CIDADE"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "CIDADE"):
                novoCidade.append(cortado[1])

        for i in cursor.execute("SELECT DISTINCT ID from dados ORDER BY ID"):
            i = str(i)
            cortado = i.split("'")
            if (cortado[1] != "ID"):
                novoViagem.append(cortado[1])

    st.session_state[1] = novoCondutores
    st.session_state[2] = novohCwb
    st.session_state[3] = novohCtb
    st.session_state[4] = novoBairro
    st.session_state[5] = novoCidade
    st.session_state[6] = novoViagem

my_map = folium.Map(location=[-25.436085, -49.269290], zoom_start=13, tiles='CartoDB positron')

condutores = [""]
hCtb = [""]
hCwb = [""]
bairro = [""]
cidade = [""]
viagem = [""]


for i in cursor.execute("SELECT DISTINCT DRIVER from dados ORDER BY DRIVER"):
    i = str(i)
    cortado = i.split("'")
    if (cortado[1] != "DRIVER"):
        condutores.append(cortado[1])

for i in cursor.execute("SELECT DISTINCT HIERARQUIA_CTB from dados ORDER BY HIERARQUIA_CTB"):
    i = str(i)
    cortado = i.split("'")
    if (cortado[1] != "HIERARQUIA_CTB"):
        hCtb.append(cortado[1])

for i in cursor.execute("SELECT DISTINCT HIERARQUIA_CWB from dados ORDER BY HIERARQUIA_CWB"):
    i = str(i)
    cortado = i.split("'")
    if (cortado[1] != "HIERARQUIA_CWB"):
        hCwb.append(cortado[1])

for i in cursor.execute("SELECT DISTINCT BAIRRO from dados ORDER BY BAIRRO"):
    i = str(i)
    cortado = i.split("'")
    if (cortado[1] != "BAIRRO"):
        bairro.append(cortado[1])

for i in cursor.execute("SELECT DISTINCT CIDADE from dados ORDER BY CIDADE"):
    i = str(i)
    cortado = i.split("'")
    if (cortado[1] != "CIDADE"):
        cidade.append(cortado[1])

for i in cursor.execute("SELECT DISTINCT ID from dados ORDER BY ID"):
    i = str(i)
    cortado = i.split("'")
    if (cortado[1] != "ID"):
        viagem.append(cortado[1])


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

atualizaInfo(dadosIndice)

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

pintaBairro(bairroSelec)

if st.sidebar.button('Refresh Page'):
    st.session_state.clear()
    st.experimental_rerun()

ignoraPrimeira = 0

folium_static(my_map, width=800, height=475)
