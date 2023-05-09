import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from matplotlib import pyplot as plt
import plotly.express as px
import altair as alt
from branca.colormap import linear

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


def transformaWeekday(weekdays):
    vetor=[]
    for dia in weekdays:
        if(dia==""):
            vetor.insert(0,dia)
        if(dia=="Domingo"):
            vetor.insert(1,dia)
        if(dia=="Segunda-feira"):
            vetor.insert(2,dia)
        if(dia=="Terça-feira"):
            vetor.insert(3,dia)
        if(dia=="Quarta-feira"):
            vetor.insert(4,dia)
        if(dia=="Quinta-Feira"):
            vetor.insert(5,dia)
        if(dia=="Sexta-feira"):
            vetor.insert(6,dia)
        if(dia=="Sábado"):
            vetor.insert(7,dia)
    return vetor


def converte(hCtb):
    vetorNominal = []
    for i in hCtb:
        if i == "":
            vetorNominal.append("")
        elif i == "1":
            vetorNominal.append("TRÂNSITO RÁPIDO")
        elif i == "2":
            vetorNominal.append("ARTERIAL")
        elif i == "3":
            vetorNominal.append("COLETORA")
        elif i == "4":
            vetorNominal.append("LOCAL")
        else:
            vetorNominal.append("NPI")
    return vetorNominal


def desconverteSing(hCtbSelec):
    if(hCtbSelec=="TRÂNSITO RÁPIDO"):
        return "1"
    elif(hCtbSelec=="ARTERIAL"):
        return "2"
    elif(hCtbSelec=="COLETORA"):
        return "3"
    elif(hCtbSelec=="LOCAL"):
        return "4"
    elif(hCtbSelec=="NPI"):
        return "NPI"
    elif(hCtbSelec==""):
        return ""
    else:
        return hCtbSelec


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
    weekdays = (pd.Series.unique(tabela["WEEKDAY"])).astype(str)
    weekdays = weekdays.tolist()
    if (param[1][1] == ""):
        weekdays.append("")
    weekdays.sort()
    bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str)
    bairros = bairros.tolist()
    if (param[2][1] == ""):
        bairros.append("")
    bairros.sort()
    hCtb = (pd.Series.unique(tabela["HIERARQUIA_CTB"])).astype(str)
    hCtb = hCtb.tolist()
    if (param[5][1] == ""):
        hCtb.append("")
    hCtb.sort()
    vsexo = (pd.Series.unique(tabela["SEXO"])).astype(str)
    vsexo = vsexo.tolist()
    if (param[4][1] == ""):
        vsexo.append("")
    vsexo.sort()
    ids = (pd.Series.unique(tabela["ID"])).astype(str)
    ids = ids.tolist()
    if (param[6][1] == ""):
        ids.append("")
    ids.sort()
    cidades = (pd.Series.unique(tabela["CIDADE"])).astype(str)
    cidades = cidades.tolist()
    if (param[7][1] == ""):
        cidades.append("")
    cidades.sort()

    st.session_state[1] = drivers
    st.session_state[2] = vsexo
    st.session_state[3] = converte(hCtb)
    st.session_state[4] = transformaWeekday(weekdays)
    st.session_state[5] = bairros
    st.session_state[6] = ids
    st.session_state[7] = idades
    st.session_state[8] = cidades



def corGeral(tabela):
    allBairros=pd.Series.unique(tabela["BAIRRO"])
    allBairros=allBairros.tolist()

    arq = open('data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")
    dfCodigo=pd.read_csv('codigoBairros.csv', sep=',')

    maxValue=0
    for i in allBairros:

        if(i!="NPI"):
            df=tabela[tabela["BAIRRO"]==i]

            linedf=dfCodigo[dfCodigo["BAIRRO"]==i]
            codigo=int(linedf["CODIGO"].iloc[0])

            dfVelocidade=df["SPD_KMH"]
            dfLimite=df["LIMITE_VEL"]
            tempoExcesso=len(df[(dfVelocidade>=dfLimite) & (dfLimite!=0)])
            tempoCorrigido=len(df[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)])
            if(tempoCorrigido!=0):
                pcExcesso=(tempoExcesso/tempoCorrigido)*10000
            else:
                pcExcesso=0
            if(pcExcesso>maxValue):
                maxValue=pcExcesso
            line=str(i)+','+str(codigo)+','+str(int(pcExcesso))+'\n'
            arq.write(line)
                
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
        line_color="Gray",
        line_opacity=0.4
    )
    choropleth.geojson.add_to(my_map)

    state_data_indexed = state_data.set_index('Codigo')

    for s in choropleth.geojson.data['features']:
        if((s['properties']['codigo']) in state_data['Codigo'].values):
            valor=s['properties']['codigo']
            s['properties']['valor'] = int(state_data_indexed.loc[valor,"Pinta"])/100
        else:
            s['properties']['valor']=0

    folium.GeoJsonTooltip(['nome', 'valor']).add_to(choropleth.geojson)

    colormap= linear.YlOrRd_09.scale(0,maxValue/100)
    colormap.caption="Percentual do tempo sob excesso de velocidade"

    colormap.add_to(my_map)





# INICIO

my_map = folium.Map(location=[-25.442027, -49.269582],
                    zoom_start=12, tiles='CartoDB positron')
map_radar = folium.Map(location=[-25.442027, -49.269582],
                    zoom_start=12, tiles='CartoDB positron')


tabela = pd.read_csv("AllFullTable.csv", sep=";", low_memory=False)

drivers = (pd.Series.unique(tabela["DRIVER"])).astype(str)
drivers = drivers.tolist()
drivers.append("")
drivers.sort()
idades = (pd.Series.unique(tabela["IDADE"])).astype(str)
idades = idades.tolist()
idades.append("")
idades.sort()
weekdays = (pd.Series.unique(tabela["WEEKDAY"])).astype(str)
weekdays = weekdays.tolist()
weekdays.append("")
weekdays.sort()
bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str)
bairros = bairros.tolist()
bairros.append("")
bairros.sort()
hCtb = (pd.Series.unique(tabela["HIERARQUIA_CTB"])).astype(str)
hCtb = hCtb.tolist()
hCtb.append("")
hCtb.sort()
vsexo = (pd.Series.unique(tabela["SEXO"])).astype(str)
vsexo = vsexo.tolist()
vsexo.append("")
vsexo.sort()
ids = (pd.Series.unique(tabela["ID"])).astype(str)
ids = ids.tolist()
ids.append("")
ids.sort()
cidades = (pd.Series.unique(tabela["CIDADE"])).astype(str)
cidades = cidades.tolist()
cidades.append("")
cidades.sort()

weekdays=transformaWeekday(weekdays)
hCtb=converte(hCtb)

if 8 not in st.session_state:
    hCtbSelec = desconverteSing(st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb))
    weekdaySelec = st.sidebar.selectbox('Dia da semana', weekdays)
    sexoSelec = st.sidebar.radio('Sexo', vsexo)
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    bairroSelec = st.sidebar.selectbox('Bairro', bairros)
    cidadeSelec = st.sidebar.selectbox('Cidade', cidades)
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    idSelec = st.sidebar.selectbox('Viagem', ids)

else:
    hCtb = st.session_state[3]
    hCtbSelec = desconverteSing(st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb))
    weekdays = st.session_state[4]
    weekdaySelec = st.sidebar.selectbox('Dia da semana', weekdays)
    vsexo = st.session_state[2]
    sexoSelec = st.sidebar.radio('Sexo', vsexo)
    idades = st.session_state[7]
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    bairros = st.session_state[5]
    bairroSelec = st.sidebar.selectbox('Bairro', bairros)
    cidades = st.session_state[8]
    cidadeSelec = st.sidebar.selectbox('Cidade', cidades)
    drivers = st.session_state[1]
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    ids = st.session_state[6]
    idSelec = st.sidebar.selectbox('Viagem', ids)

param = []
param.append([0, driverSelec])
param.append([1, weekdaySelec])
param.append([2, bairroSelec])
param.append([3, idadeSelec])
param.append([4, sexoSelec])
param.append([5, hCtbSelec])
param.append([6, idSelec])
param.append([7, cidadeSelec])

resul = tabela

for i in param:
    if (i[0] == 0 and (i[1] != "")):
        resul = resul[resul["DRIVER"] == i[1]]
    if (i[0] == 1 and (i[1] != "")):
        resul = resul[resul["WEEKDAY"] == i[1]]
    if (i[0] == 2 and (i[1] != "")):
        resul = resul[resul["BAIRRO"] == i[1]]
    if (i[0] == 3 and (i[1] != "")):
        resul = resul[resul["IDADE"] == i[1]]
    if (i[0] == 4 and (i[1] != "")):
        resul = resul[resul["SEXO"] == i[1]]
    if (i[0] == 5 and (i[1] != "")):
        resul = resul[resul["HIERARQUIA_CTB"] == i[1]]
    if (i[0] == 6 and (i[1] != "")):
        resul = resul[resul["ID"] == i[1]]
    if (i[0] == 7 and (i[1] != "")):
        resul = resul[resul["CIDADE"] == i[1]]

atualizaInfo(resul, param)

if (st.session_state[1] != drivers):
    st.experimental_rerun()
if (st.session_state[2] != vsexo):
    st.experimental_rerun()
if (st.session_state[3] != hCtb):
    st.experimental_rerun()
if (st.session_state[4] != weekdays):
    st.experimental_rerun()
if (st.session_state[5] != bairros):
    st.experimental_rerun()
if (st.session_state[6] != ids):
    st.experimental_rerun()
if (st.session_state[7] != idades):
    st.experimental_rerun()
if (st.session_state[8] != cidades):
    st.experimental_rerun()


if st.sidebar.button('Refresh Page'):
    st.session_state.clear()
    st.experimental_rerun()



dfValid=resul["VALID_TIME"].astype(int)
tempoValidoEspecifico=(dfValid.sum(axis=0))

dfVelocidade=resul["SPD_KMH"]
dfLimite=resul["LIMITE_VEL"]

dfExcesso=resul[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
tempoExcesso=len(dfExcesso)
percentualExcesso=round((tempoExcesso/tempoValidoEspecifico*100),2)

dfCorrigido=resul[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
tempoCorrigido=len(dfCorrigido)
percentualOportunidade=round((tempoCorrigido/tempoValidoEspecifico*100),2)

if(tempoCorrigido!=0):
    excessoCorrigido=round((tempoExcesso/tempoCorrigido*100),2)
else:
    excessoCorrigido=0

col1, col2, col3= st.columns(3)
with col1:
    st.metric("\\% do tempo sob excesso de velocidade em relação ao tempo total de viagem", str(percentualExcesso)+"%")
with col2:
    st.metric("\\% do tempo de viagem com oportunidade de excesso de velocidade", str(percentualOportunidade)+"%")
with col3:
    st.metric("\\% do tempo sob excesso de velocidade em relação ao tempo de viagem*", str(excessoCorrigido)+"%")




cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str)
cidades = cidades.tolist()
percentCidades = []
cidadesOfc = []

for i in cidades:
    dfCidade = resul[resul["CIDADE"] == i]
    dfValid=dfCidade["VALID_TIME"].astype(int)
    tempoValidoEspecifico=(dfValid.sum(axis=0))

    dfVelocidade=dfCidade["SPD_KMH"]
    dfLimite=dfCidade["LIMITE_VEL"]

    dfExcesso=dfCidade[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    tempoExcesso=len(dfExcesso)

    dfCorrigido=dfCidade[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
    tempoCorrigido=len(dfCorrigido)

    if(tempoCorrigido!=0):
        excessoCorrigido=round((tempoExcesso/tempoCorrigido*100),2)
    else:
        excessoCorrigido=0

    if(excessoCorrigido>0):
        percentCidades.append(excessoCorrigido)
        cidadesOfc.append(i)


data = {"CIDADE": cidadesOfc, "PERCENTUAL": percentCidades}
new_df = pd.DataFrame(data)
dfCidade = new_df.sort_values(["PERCENTUAL"])

st.subheader("\\% do tempo sob excesso de velocidade por cidade*")
bars = alt.Chart(dfCidade).mark_bar(width=20).encode(
    x='PERCENTUAL',
    y=alt.Y("CIDADE",sort='x') 
)
st.altair_chart(bars)

bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str)
bairros = bairros.tolist()

percentBairros = []
bairrosOfc = []

for i in bairros:
    dfBairro = resul[resul["BAIRRO"] == i]
    dfValid=dfBairro["VALID_TIME"].astype(int)
    tempoValidoEspecifico=(dfValid.sum(axis=0))

    dfVelocidade=dfBairro["SPD_KMH"]
    dfLimite=dfBairro["LIMITE_VEL"]

    dfExcesso=dfBairro[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    tempoExcesso=len(dfExcesso)

    dfCorrigido=dfBairro[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
    tempoCorrigido=len(dfCorrigido)

    if(tempoCorrigido!=0):
        excessoCorrigido=round((tempoExcesso/tempoCorrigido*100),2)
    else:
        excessoCorrigido=0
        
    if(excessoCorrigido>0):
        percentBairros.append(excessoCorrigido)
        bairrosOfc.append(i)


data = {"BAIRRO": bairrosOfc, "PERCENTUAL": percentBairros}
new_df = pd.DataFrame(data)
dfBairro = new_df.sort_values(["PERCENTUAL"])

st.subheader("\\% do tempo sob excesso de velocidade por bairro de Curitiba*")
bars = alt.Chart(dfBairro).mark_bar(width=20).encode(
    x='PERCENTUAL',
    y=alt.Y("BAIRRO",sort='x') 
)
st.altair_chart(bars)


limites = ((pd.Series.unique(tabela["LIMITE_VEL"]))).astype(str)
limites = limites.tolist()

percentVia = []
limiteVias = []

for i in limites:
    dfLm = resul[resul["LIMITE_VEL"] == int(i)]
    dfValid=dfLm["VALID_TIME"].astype(int)
    tempoValidoEspecifico=(dfValid.sum(axis=0))

    dfVelocidade=dfLm["SPD_KMH"]
    dfLimite=dfLm["LIMITE_VEL"]

    dfExcesso=dfLm[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    tempoExcesso=len(dfExcesso)

    dfCorrigido=dfLm[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
    tempoCorrigido=len(dfCorrigido)

    if(tempoCorrigido!=0):
        excessoCorrigido=round((tempoExcesso/tempoCorrigido*100),2)
    else:
        excessoCorrigido=0
        
    if(excessoCorrigido>0):
        percentVia.append(excessoCorrigido)
        limiteVias.append(i)


data = {"LIMITE VIA": limiteVias, "PERCENTUAL": percentVia}
new_df = pd.DataFrame(data)
dfLimite = new_df.sort_values(["PERCENTUAL"])

st.subheader("\\% do tempo sob excesso de velocidade segundo limite de velocidade regulamentar da via*")
bars = alt.Chart(dfLimite).mark_bar(width=20).encode(
    x='PERCENTUAL',
    y=alt.Y("LIMITE VIA",sort='-x') 
)
st.altair_chart(bars)

corGeral(resul)

radares=pd.read_csv("radares.csv",sep=",")
for i,j in radares.iterrows():
    if 'LOMBADA' in j['Tipo']:
        longitude=float(j['Longitude'])
        latitude=float(j['Latitude'])
        folium.Circle([latitude, longitude], 15,
            color='blue', fill_color="blue", fill_opacity=0.7).add_to(map_radar)
    elif 'RADAR' in j['Tipo']:
        longitude=float(j['Longitude'])
        latitude=float(j['Latitude'])
        folium.Circle([latitude, longitude], 15,
            color='red', fill_color="red", fill_opacity=0.7).add_to(map_radar)

folium_static(my_map)

folium_static(map_radar)
