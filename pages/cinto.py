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


def atualizaInfo(tabela, param):
    idades = (pd.Series.unique(tabela["IDADE"])).astype(str)
    idades = idades.tolist()
    if (param[0][1] == ""):
        idades.append("")
    idades.sort()
    vsexo = (pd.Series.unique(tabela["SEXO"])).astype(str)
    vsexo = vsexo.tolist()
    if (param[1][1] == ""):
        vsexo.append("")
    vsexo.sort()
    drivers = (pd.Series.unique(tabela["DRIVER"])).astype(str)
    drivers = drivers.tolist()
    if (param[2][1] == ""):
        drivers.append("")
    drivers.sort()
    ids = (pd.Series.unique(tabela["ID"])).astype(str)
    ids = ids.tolist()
    if (param[3][1] == ""):
        ids.append("")
    ids.sort()

    st.session_state[1] = idades
    st.session_state[2] = vsexo
    st.session_state[3] = drivers
    st.session_state[10] = ids



def corGeral(tabela,escolhaLimite):
    allBairros=pd.Series.unique(tabela["BAIRRO"])
    allBairros=allBairros.tolist()

    arq = open('data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")
    dfCodigo=pd.read_csv('codigoBairros.csv', sep=',')

    maxValue=0
    for i in allBairros:

        if(i!="NPI"):
            df=tabela[tabela["BAIRRO"]==i]

            dfVelocidade=df["SPD_KMH"]
            dfLimite=df["LIMITE_VEL"]
            if(escolhaLimite=="Acima do limite de velocidade"):
                df=df[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
            elif (escolhaLimite=="Abaixo do limite de velocidade"):
                df=df[(dfVelocidade<=dfLimite) & (dfLimite!=0)]

            dfValidEsp=df["VALID_TIME"].astype(int)
            tempoValidoEspecifico=(dfValidEsp.sum(axis=0))

            linedf=dfCodigo[dfCodigo["BAIRRO"]==i]
            codigo=int(linedf["CODIGO"].iloc[0])

            qntWsb=df["WSB"].astype(int).sum(axis=0)
            if(tempoValidoEspecifico!=0):
                percentWsb=(1-(qntWsb/tempoValidoEspecifico))*10000
            else:
                percentWsb=0
            if(percentWsb>maxValue):
                maxValue=percentWsb
            line=str(i)+','+str(codigo)+','+str(int(percentWsb))+'\n'
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

    folium.GeoJsonTooltip(['nome', 'valor']).add_to(choropleth.geojson)

    colormap= linear.YlOrRd_09.scale(0,maxValue/100)
    colormap.caption="Percentual do tempo sem o uso do cinto de segurança"
    colormap.add_to(my_map)




# INICIO

my_map = folium.Map(location=[-25.442027, -49.269582],
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
vsexo = (pd.Series.unique(tabela["SEXO"])).astype(str)
vsexo = vsexo.tolist()
vsexo.append("")
vsexo.sort()
ids = (pd.Series.unique(tabela["ID"])).astype(str)
ids = ids.tolist()
ids.append("")
ids.sort()

# Utilizado sessão 10 devido erros ao trocar de página
if 10 not in st.session_state:
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    sexoSelec = st.sidebar.radio('Sexo', vsexo)
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    idSelec = st.sidebar.selectbox('Viagem', ids)

else:
    idades = st.session_state[1]
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    vsexo = st.session_state[2]
    sexoSelec = st.sidebar.radio('Sexo', vsexo)
    drivers = st.session_state[3]
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    ids = st.session_state[10]
    idSelec = st.sidebar.selectbox('Viagem', ids)

param = []
param.append([0, idadeSelec])
param.append([1, sexoSelec])
param.append([2, driverSelec])
param.append([3, idSelec])

resul = tabela

for i in param:
    if (i[0] == 0 and (i[1] != "")):
        resul = resul[resul["IDADE"] == i[1]]
    if (i[0] == 1 and (i[1] != "")):
        resul = resul[resul["SEXO"] == i[1]]
    if (i[0] == 2 and (i[1] != "")):
        resul = resul[resul["DRIVER"] == i[1]]
    if (i[0] == 3 and (i[1] != "")):
        resul = resul[resul["ID"] == i[1]]

atualizaInfo(resul, param)

if (st.session_state[1] != idades):
    st.experimental_rerun()
if (st.session_state[2] != vsexo):
    st.experimental_rerun()
if (st.session_state[3] != drivers):
    st.experimental_rerun()
if (st.session_state[10] != ids):
    st.experimental_rerun()


if st.sidebar.button('Refresh Page'):
    st.session_state.clear()
    st.experimental_rerun()


dfValid=resul["VALID_TIME"].astype(int)
tempoValidoEspecifico=(dfValid.sum(axis=0))


dfWsb=resul["WSB"].astype(int)
qntWsb=(dfWsb.sum(axis=0))

percentWsb=round(((qntWsb/tempoValidoEspecifico)*100),2)

dfUsoCinto = resul[resul["WSB"]==1]
vmUsoCinto=round(((dfUsoCinto["SPD_KMH"].sum(axis=0))/len(dfUsoCinto)),2)

dfSemCinto=resul[resul["WSB"]==0]
vmSemCinto=round(((dfSemCinto["SPD_KMH"].sum(axis=0))/len(dfSemCinto)),2)

col1, col2, col3= st.columns(3)
with col1:
    st.metric("Percentual de uso do cinto de segurança", str(percentWsb)+"%")
with col2:
    st.metric("Velocidade média com o uso do cinto (km/h)", vmUsoCinto)
with col3:
    st.metric("Velocidade média sem o uso do cinto (km/h)", vmSemCinto)


hierarquias = ((pd.Series.unique(tabela["HIERARQUIA_CTB"]))).astype(str)
hierarquias = hierarquias.tolist()
hctbs=[]
percentHctbs=[]
for i in hierarquias:
    df = resul[resul["HIERARQUIA_CTB"] == i]
    dfValid=df["VALID_TIME"].astype(int)
    tempoValidoEspecifico=(dfValid.sum(axis=0))

    dfWsb=(df["WSB"]==0).astype(int)
    qntWsb=(dfWsb.sum(axis=0))

    percentWsb=round(((qntWsb/tempoValidoEspecifico)*100),2)
    percentHctbs.append(percentWsb)
    hctbs.append(i)

df=pd.DataFrame({"HIERARQUIA":hctbs, "Porcentagem sem cinto":percentHctbs})
df = df.set_index("HIERARQUIA")
bar_chart=st.bar_chart(df)

cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str)
cidades = cidades.tolist()

percentCidades = []
cidadesOfc = []

for i in cidades:
    dfCidade = resul[resul["CIDADE"] == i]
    dfValid=dfCidade["VALID_TIME"].astype(int)
    tempoValidoEspecifico=(dfValid.sum(axis=0))

    dfWsb=dfCidade["WSB"].astype(int)
    qntWsb=(dfWsb.sum(axis=0))

    percentWsb=round(((qntWsb/tempoValidoEspecifico)*100),2)
    if(percentWsb>0):
        cidadesOfc.append(i)
        percentCidades.append(percentWsb)

data = {"CIDADE": cidadesOfc, "FREQUENCIA": percentCidades}
new_df = pd.DataFrame(data)
dfCidade = new_df.sort_values(["FREQUENCIA"])



bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str)
bairros = bairros.tolist()
percentBairros = []
bairrosOfc = []
for i in bairros:
    dfBairro = resul[resul["BAIRRO"] == i]
    dfValid=dfBairro["VALID_TIME"].astype(int)
    tempoValidoEspecifico=(dfValid.sum(axis=0))

    dfWsb=dfBairro["WSB"].astype(int)
    qntWsb=(dfWsb.sum(axis=0))

    percentWsb=round(((qntWsb/tempoValidoEspecifico)*100),2)
    bairrosOfc.append(i)
    percentBairros.append(percentWsb)

data = {"BAIRRO": bairrosOfc, "FREQUENCIA": percentBairros}

new_df = pd.DataFrame(data)
dfBairro = new_df.sort_values(["FREQUENCIA"])



st.subheader("Percentual do tempo de viagem usando o cinto de segurança")
bars = alt.Chart(dfCidade).mark_bar(width=20).encode(
    x='FREQUENCIA',
    y=alt.Y("CIDADE",sort='x') 
)
st.altair_chart(bars)



st.subheader("Percentual do tempo de viagem usando o cinto de segurança")
bars = alt.Chart(dfBairro).mark_bar(width=20).encode(
    x='FREQUENCIA',
    y=alt.Y("BAIRRO",sort='x') 
)
st.altair_chart(bars)


options=["Independente do limite de velocidade","Abaixo do limite de velocidade","Acima do limite de velocidade"]
escolhaLimite=st.radio("",options)

corGeral(tabela,escolhaLimite)


st.subheader("Porcentagem do tempo de viagem sem o uso do cinto de segurança segundo bairro de Curitiba")
folium_static(my_map)
