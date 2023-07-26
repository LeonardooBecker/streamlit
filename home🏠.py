import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from branca.colormap import linear
import json
import math

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)
    
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
    else:
        return ""

def corGeral(escolha, tabela):
    allBairros = pd.Series.unique(tabela["BAIRRO"])
    allBairros = allBairros.tolist()

    arq = open('data.csv', 'w')
    arq.write("Bairros,Codigo,Pinta\n")
    dfCodigo = pd.read_csv('codigoBairros.csv', sep=',')

    maxValue = 0
    for i in allBairros:

        if (i != "NPI"):
            df = tabela[tabela["BAIRRO"] == i]

            dfValidEsp = df["VALID_TIME"].astype(int)
            tempoValidoEspecifico = (dfValidEsp.sum(axis=0))

            tempoValidoTotal = (tabela["VALID_TIME"].astype(int)).sum(axis=0)

            linedf = dfCodigo[dfCodigo["BAIRRO"] == i]
            codigo = int(linedf["CODIGO"].iloc[0])

            if (escolha == "Frequência de uso do celular (usos/hora)"):
                qntPickUps = ((df["PICK_UP"]).astype(int)).sum(axis=0)
                freqUso = (qntPickUps/(tempoValidoTotal/3600))*1000
                if (freqUso > maxValue):
                    maxValue = freqUso
                line = str(i)+","+str(codigo)+","+str(int(freqUso))+"\n"
                arq.write(line)

            if (escolha == "Percentual do tempo de não uso do cinto de segurança"):
                qntWsb = df["WSB"].astype(int).sum(axis=0)
                percentWsb = (1-(qntWsb/tempoValidoEspecifico))*10000
                if (percentWsb > maxValue):
                    maxValue = percentWsb
                line = str(i)+','+str(codigo)+','+str(int(percentWsb))+'\n'
                arq.write(line)

            if (escolha == "Percentual do tempo sob excesso de velocidade*"):
                dfVelocidade = df["SPD_KMH"]
                dfLimite = df["LIMITE_VEL"]
                tempoExcesso = len(
                    df[(dfVelocidade >= dfLimite) & (dfLimite != 0)])
                tempoCorrigido = len(
                    df[(dfVelocidade >= (dfLimite-10)) & (dfLimite != 0)])
                if (tempoCorrigido != 0):
                    pcExcesso = (tempoExcesso/tempoCorrigido)*10000
                else:
                    pcExcesso = 0
                if (pcExcesso > maxValue):
                    maxValue = pcExcesso
                line = str(i)+','+str(codigo)+','+str(int(pcExcesso))+'\n'
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

    if (escolha == "Frequência de uso do celular (usos/hora)"):
        colormap = linear.YlOrRd_09.scale(0, maxValue/1000)
        colormap.caption = "Frequência de uso do celular por hora"

    if (escolha == "Percentual do tempo de não uso do cinto de segurança"):
        colormap = linear.YlOrRd_09.scale(0, maxValue/100)
        colormap.caption = "Percentual do tempo sem o uso do cinto de segurança"

    if (escolha == "Percentual do tempo sob excesso de velocidade*"):
        colormap = linear.YlOrRd_09.scale(0, maxValue/100)
        colormap.caption = "Percentual do tempo sob excesso de velocidade"

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
    st.session_state[3] = converte(hCtb)
    st.session_state[4] = bairros
    st.session_state[5] = cidades
    st.session_state[6] = ids
    st.session_state[7] = idades


my_map = folium.Map(location=[-25.442027, -49.269582],
                    zoom_start=12)

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

hCtb=converte(hCtb)

if 7 not in st.session_state:
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    hCwbSelec = st.sidebar.selectbox('Hierarquia viária (Curitiba)', hCwb)
    hCtbSelec = desconverteSing(st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb))
    bairroSelec = st.sidebar.selectbox('Bairro', bairros)
    cidadeSelec = st.sidebar.selectbox('Cidade', cidades)
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    idSelec = st.sidebar.selectbox('Viagem', ids)

else:
    idades = st.session_state[7]
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    hCwb = st.session_state[2]
    hCwbSelec = st.sidebar.selectbox('Hierarquia viária (Curitiba)', hCwb)
    hCtb = st.session_state[3]
    hCtbSelec = desconverteSing(st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb))
    bairros = st.session_state[4]
    bairroSelec = st.sidebar.selectbox('Bairro', bairros)
    cidades = st.session_state[5]
    cidadeSelec = st.sidebar.selectbox('Cidade', cidades)
    drivers = st.session_state[1]
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    ids = st.session_state[6]
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


if st.sidebar.button('Atualizar página'):
    st.session_state.clear()
    st.experimental_rerun()

## Título da página

st.markdown("""
            <style>
            .titulo {
                display: flex;
            }
            #texto{
                padding: 10px;
            }
            #logoNDS {
                display: block;
                width: 40%;
                height: fit-content;
                margin: auto;
                padding: 15px;
            }
            </style>
            <div class="titulo">
                <h1 style="font-size:42px; text-align:center">Estudo Naturalístico de Direção Brasileiro</h1>
                <img src='https://www.inf.ufpr.br/lbo21/images/logoBranca.png' id="logoNDS">
            </div>
            <hr>
            """, unsafe_allow_html=True)

##---------------------------------------------


dfValid=resul["VALID_TIME"].astype(int)
tempoValidoEspecifico=(dfValid.sum(axis=0))

dfPick=resul["PICK_UP"].astype(int)
qntPickUp=(dfPick.sum(axis=0))


freqUsoCelular=round((qntPickUp/(tempoValidoEspecifico/3600)),2)


dfWsb=resul["WSB"].astype(int)
qntWsb=(dfWsb.sum(axis=0))

percentWsb=round(((1-qntWsb/tempoValidoEspecifico)*100),2)


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
    st.metric("Frequência de uso do celular (usos/hora)",freqUsoCelular)
with col2:
    st.metric("Percentual do tempo de não uso do cinto de segurança",str(percentWsb)+"%")
with col3:
    st.metric("Percentual do tempo sob excesso de velocidade*",str(pcExcesso)+"%")
with col4:
    st.metric("Tempo de viagem (h)",round((tempoValidoEspecifico/3600),2))


options=["Frequência de uso do celular (usos/hora)","Percentual do tempo de não uso do cinto de segurança","Percentual do tempo sob excesso de velocidade*"]

if 'escolha' not in st.session_state:
    st.session_state.escolha = options[0]

# Botão de seleção
escolha = st.selectbox("",options, index=options.index(st.session_state.escolha))

# Verificar se houve alteração na opção selecionada
if escolha != st.session_state.escolha:
    # Atualizar a opção selecionada no st.session_state
    st.session_state.escolha = escolha
    # Rerun do aplicativo
    st.experimental_rerun()

corGeral(st.session_state.escolha,resul)

if(escolha=="Frequência de uso do celular (usos/hora)"):
    st.subheader("Mapa de calor representando a frequência de uso do celular por hora")

if(escolha=="Percentual do tempo de não uso do cinto de segurança"):
    st.subheader("Mapa de calor representando o percentual do tempo sem o uso do cinto de segurança")

if(escolha=="Percentual do tempo sob excesso de velocidade*"):
    st.subheader("Mapa de calor representando o percentual do tempo sob o excesso de velocidade")


# if(escolha=="Frequência de uso do celular (usos/hora)"):
#     usandoCelular=resul[(dfPick==1)]
#     for linha, dados in usandoCelular.iterrows():
#         longitude=float((dados[1]))
#         latitude=float(dados[2])
#         if not (math.isnan(longitude) or math.isnan(latitude)):
#             folium.Circle([latitude, longitude], 3,
#                     color='red', fill_color="red", fill_opacity=1).add_to(my_map)


# if(escolha=="Percentual do tempo de não uso do cinto de segurança"):
#     semCinto=(resul[(dfWsb==0)])            
#     for linha, dados in semCinto.iterrows():
#         longitude=float((dados[1]))
#         latitude=float(dados[2])
#         if not (math.isnan(longitude) or math.isnan(latitude)):
#             folium.Circle([latitude, longitude], 3,
#                     color='red', fill_color="red", fill_opacity=1).add_to(my_map)

# if(escolha=="Percentual do tempo sob excesso de velocidade*"):
#     # dfExcesso definido quando foi usado para caluclar o paramentro de percentual de excesso de velocidade ( nao houve alteracoes no dataframe )
#     for linha, dados in dfExcesso.iterrows():
#         longitude=float((dados[1]))
#         latitude=float(dados[2])
#         if not (math.isnan(longitude) or math.isnan(latitude)):
#             folium.Circle([latitude, longitude], 3,
#                     color='red', fill_color="red", fill_opacity=1).add_to(my_map)
            

# if(escolha=="Frequência de uso do celular (usos/hora)"):
#     st.subheader("Pontos referentes aos locais onde houve utilização do celular")

# if(escolha=="Percentual do tempo de não uso do cinto de segurança"):
#     st.subheader("Pontos referentes aos locais onde não houve a utilização do cinto de segurança")

# if(escolha=="Percentual do tempo sob excesso de velocidade*"):
#     st.subheader("Pontos referentes aos locais onde houve o excesso de velocidade")

folium_static(my_map)

## Rodapé da página

st.markdown("""
            <style>
            .back
            {
                padding: 30px;
                border-radius: 20px;
                background-color: #c8c8c8;
            }
            #infos {
                color: #353535;
            }
            #refs
            {
                color: #666666;
                margin: 30px;
            }
            .images {
                display: flex;
                flex-wrap: wrap;
            }
            .images img {
                width:30%;
                padding: 20px;
                flex: 1;
                object-fit: contain; 
            }
            </style>
            <hr>
            <div class="back">
                <div id="infos">
                    <p style="margin:2px; font-size: 14px;">Desenvolvedor: Leonardo Becker de Oliveira <a href="mailto:lbo21@inf.ufpr.br"> lbo21@inf.ufpr.br </a></p>
                    <p style="margin:2px; font-size: 14px;">Coordenador: Prof. Dr. Jorge Tiago Bastos <a href="mailto:jtbastos@ufpr.br"> jtbastos@ufpr.br </a></p>
                    <p style="margin:2px; font-size: 14px;">Financiamento: Universidade Federal do Paraná, Conselho Nacional de Desenvolvimento Científico e Tecnológico, Observatório Nacional de Segurança Viária e Mobi 7 - Soluções para Mobilidade.</p>
                    <p style="margin:2px; font-size: 14px;">Mais informações em <a href="http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/">Estudo Naturalístico de Direção Brasileiro - CEPPUR-UFPR</a> (Link para este endereço: <a href="http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/">http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/</a> )</p>
                </div>
                <div id="refs">     
                    <p style="font-size: 12px; margin:2px">* % do tempo sob excesso de velocidade em relação ao tempo de viagem com oportunidade de excesso de velocidade</p>
                    <p style="font-size: 12px; margin:2px"> Para referenciar este conteúdo: OLIVEIRA, Leonardo Becker; BASTOS, Jorge Tiago. Estudo Naturalístico de Direção Brasileiro: Painel de visualização. Curitiba 2023. Disponível em: <a href="https://painelndsbr.streamlit.app">Streamlit</a>. Acesso em: dia mês. ano. </p>
                </div>
                <div class="images">
                    <img src="https://www.inf.ufpr.br/lbo21/images/logoUFPR.jpg">
                    <img src="https://www.inf.ufpr.br/lbo21/images/logoCNPQ.jpg">
                    <img src="https://www.inf.ufpr.br/lbo21/images/logoONSV.png">
                </div>
            </div>
             """ , unsafe_allow_html=True
            )