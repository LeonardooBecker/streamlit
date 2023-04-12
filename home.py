import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from branca.colormap import linear
import json

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


def pintaBairro(bairroSelec):
    # Escreve a primeira linha, padrao para qualquer tipo de bairro ( inclusive o NULL )
    arq = open('bairroSelec.csv', 'w')
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

    state_data = pd.read_csv('bairroSelec.csv', encoding='latin-1')

    if(bairroSelec!=""):
        choropleth = folium.Choropleth(
            geo_data='bairros.geo.json',
            data=state_data,
            columns=['Codigo', 'Pinta'],
            key_on='feature.properties.codigo',
            fill_color="Greys",
            fill_opacity=0.7,
            nan_fill_opacity=0.2,
            nan_fill_color="White",
            line_opacity=0.5,
            line_color="Gray"
        )
        choropleth.geojson.add_to(my_map)



def corGeral(esolha,tabela):
    allBairros=pd.Series.unique(tabela["BAIRRO"])
    allBairros=allBairros.tolist()

    arq = open('data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")
    dfCodigo=pd.read_csv('codigoBairros.csv', sep=',')

    maxValue=0
    for i in allBairros:

        if(i!="NPI"):
            df=tabela[tabela["BAIRRO"]==i]

            dfValidEsp=df["VALID_TIME"].astype(int)
            tempoValidoEspecifico=(dfValidEsp.sum(axis=0))

            tempoValidoTotal=(tabela["VALID_TIME"].astype(int)).sum(axis=0)

            linedf=dfCodigo[dfCodigo["BAIRRO"]==i]
            codigo=int(linedf["CODIGO"].iloc[0])

            if(escolha=="Frequência de uso do celular (uso/hora)"):
                qntPickUps=((df["PICK_UP"]).astype(int)).sum(axis=0)
                freqUso=(qntPickUps/(tempoValidoTotal/3600))*1000
                if(freqUso>maxValue):
                    maxValue=freqUso
                line=str(i)+","+str(codigo)+","+str(int(freqUso))+"\n"
                arq.write(line)

            if(escolha=="Percentual do tempo de uso do cinto de segurança"):
                qntWsb=df["WSB"].astype(int).sum(axis=0)
                percentWsb=(1-(qntWsb/tempoValidoEspecifico))*10000
                if(percentWsb>maxValue):
                    maxValue=percentWsb
                line=str(i)+','+str(codigo)+','+str(int(percentWsb))+'\n'
                arq.write(line)

            if(escolha=="Percentual do tempo sob excesso de velocidade*"):
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
            if(escolha=="Frequência de uso do celular (uso/hora)"):
                s['properties']['valor'] = int(state_data_indexed.loc[valor,"Pinta"])/1000
            else:
                s['properties']['valor'] = int(state_data_indexed.loc[valor,"Pinta"])/100

    folium.GeoJsonTooltip(['nome', 'valor']).add_to(choropleth.geojson)


    if(escolha=="Frequência de uso do celular (uso/hora)"):
        colormap= linear.YlOrRd_09.scale(0,maxValue/1000)
        colormap.caption="Frequência de uso do celular por hora"

    if(escolha=="Percentual do tempo de uso do cinto de segurança"):
        colormap= linear.YlOrRd_09.scale(0,maxValue/100)
        colormap.caption="Percentual do tempo sem o uso do cinto de segurança"

    if(escolha=="Percentual do tempo sob excesso de velocidade*"):
        colormap= linear.YlOrRd_09.scale(0,maxValue/100)
        colormap.caption="Percentual do tempo sob excesso de velocidade"

    colormap.add_to(my_map)


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

dfValid=tabela["VALID_TIME"].astype(int)
tempoValidoTotal=(dfValid.sum(axis=0))
tempoValidoTotal=round((tempoValidoTotal/3600),2)

dfValid=resul["VALID_TIME"].astype(int)
tempoValidoEspecifico=(dfValid.sum(axis=0))

dfPick=resul["PICK_UP"].astype(int)
qntPickUp=(dfPick.sum(axis=0))


freqUsoCelular=round((qntPickUp/tempoValidoTotal),2)


dfWsb=resul["WSB"].astype(int)
qntWsb=(dfWsb.sum(axis=0))

percentWsb=round(((qntWsb/tempoValidoEspecifico)*100),2)


dfVelocidade=resul["SPD_KMH"]
dfLimite=resul["LIMITE_VEL"]

dfExcesso=resul[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
tempoExcesso=len(dfExcesso)

dfCorrigido=resul[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
tempoCorrigido=len(dfCorrigido)

if(tempoCorrigido!=0):
    pcExcesso=round((tempoExcesso/tempoCorrigido*100),2)
else:
    pcExcesso=0

col1, col2, col3, col4= st.columns(4)

with col1:
    st.metric("Frequência de uso do celular (uso/hora)",freqUsoCelular)
with col2:
    st.metric("Percentual do tempo de uso do cinto de segurança",str(percentWsb)+"%")
with col3:
    st.metric("Percentual do tempo sob excesso de velocidade*",str(pcExcesso)+"%")
with col4:
    st.metric("Tempo de viagem (h)",round((tempoValidoEspecifico/3600),2))

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


if st.sidebar.button('Refresh Page'):
    st.session_state.clear()
    st.experimental_rerun()


pintaBairro(bairroSelec)

options=["Frequência de uso do celular (uso/hora)","Percentual do tempo de uso do cinto de segurança","Percentual do tempo sob excesso de velocidade*"]

escolha=st.selectbox("",options)

pinta=1
for i in param:
    if(i[1]!=""):
       pinta=0

if pinta:
    if(escolha=="Frequência de uso do celular (uso/hora)"):
        st.subheader("Mapa de calor representando a frequência de uso do celular por hora")

    if(escolha=="Percentual do tempo de uso do cinto de segurança"):
        st.subheader("Mapa de calor representando o percentual do tempo sem o uso do cinto de segurança")

    if(escolha=="Percentual do tempo sob excesso de velocidade*"):
        st.subheader("Mapa de calor representando o tempo sob o excesso de velocidade")

    corGeral(options,tabela)
else:
    if(escolha=="Frequência de uso do celular (uso/hora)"):
        usandoCelular=resul[(dfPick==1)]
        for linha, dados in usandoCelular.iterrows():
            longitude=float((dados[1]))
            latitude=float(dados[2])
            folium.Circle([latitude, longitude], 3,
                        color='red', fill_color="red", fill_opacity=1).add_to(my_map)


    if(escolha=="Percentual do tempo de uso do cinto de segurança"):
        semCinto=(resul[(dfWsb==0)])            
        for linha, dados in semCinto.iterrows():
            longitude=float((dados[1]))
            latitude=float(dados[2])
            folium.Circle([latitude, longitude], 3,
                        color='red', fill_color="red", fill_opacity=1).add_to(my_map)

    if(escolha=="Percentual do tempo sob excesso de velocidade*"):
        # dfExcesso definido quando foi usado para caluclar o paramentro de percentual de excesso de velocidade ( nao houve alteracoes no dataframe )
        for linha, dados in dfExcesso.iterrows():
            longitude=float((dados[1]))
            latitude=float(dados[2])
            folium.Circle([latitude, longitude], 3,
                        color='red', fill_color="red", fill_opacity=1).add_to(my_map)
            
    if(escolha=="Frequência de uso do celular (uso/hora)"):
        st.subheader("Pontos referentes aos locais onde houve utilização do celular")

    if(escolha=="Percentual do tempo de uso do cinto de segurança"):
        st.subheader("Pontos referentes aos locais onde não houve a utilização do cinto de segurança")

    if(escolha=="Percentual do tempo sob excesso de velocidade*"):
        st.subheader("Pontos referentes aos locais onde houve o excesso de velocidade")


folium_static(my_map)
