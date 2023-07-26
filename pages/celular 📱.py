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

def tradutor(word):
    if(word=="CHECKING/BROWSING"):
        return "CONFERINDO/NAVEGANDO"
    if(word=="ON-HOLDER"):
        return "USO NO SUPORTE"
    if(word=="HOLDING"):
        return "SEGURANDO"
    if(word=="TEXTING"):
        return "ENVIANDO MENSAGEM"
    if(word=="CALLING/VOICE MESSAGE"):
        return "LIGAÇÃO/MENSAGEM DE VOZ"
    if(word=="OTHER"):
        return "OUTROS"     
    if(word=="NPI"):
        return "NPI"
    return word

def voltaTradutor(word):
    if(word=="CONFERINDO/NAVEGANDO"):
        return "CHECKING/BROWSING"
    elif(word=="USO NO SUPORTE"):
        return "ON-HOLDER"
    elif(word=="SEGURANDO"):
        return "HOLDING"
    elif(word=="ENVIANDO MENSAGEM"):
        return "TEXTING"
    elif(word=="LIGAÇÃO/MENSAGEM DE VOZ"):
        return "CALLING/VOICE MESSAGE"
    elif(word=="OUTROS"):
        return "OTHER"  
    elif(word=="NPI"):
        return "NPI"
    return word


def traduzVetor(usos):
    vetorTraduzido=[]
    for word in usos:
        if(word==""):
            vetorTraduzido.append("")
        elif(word=="CHECKING/BROWSING"):
            vetorTraduzido.append("CONFERINDO/NAVEGANDO")
        elif(word=="ON-HOLDER"):
            vetorTraduzido.append("USO NO SUPORTE")
        elif(word=="HOLDING"):
            vetorTraduzido.append("SEGURANDO")
        elif(word=="TEXTING"):
            vetorTraduzido.append("ENVIANDO MENSAGEM")
        elif(word=="CALLING/VOICE MESSAGE"):
            vetorTraduzido.append("LIGAÇÃO/MENSAGEM DE VOZ")
        elif(word=="OTHER"):
            vetorTraduzido.append("OUTROS")
        elif(word=="NPI"):
            vetorTraduzido.append("NPI")
    return vetorTraduzido


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
    usos = ((pd.Series.unique(tabela["ACTION"]))).astype(str)
    usos = usos.tolist()
    if (param[2][1] == ""):
        usos.append("")
    usos.sort()
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
    categorias = (pd.Series.unique(tabela["CATEGORIA"])).astype(str)
    categorias = categorias.tolist()
    if (param[7][1] == ""):
        categorias.append("")
    categorias.sort()

    st.session_state[1] = drivers
    st.session_state[2] = vsexo
    st.session_state[3] = converte(hCtb)
    st.session_state[4] = transformaWeekday(weekdays)
    st.session_state[5] = traduzVetor(usos)
    st.session_state[6] = ids
    st.session_state[7] = idades
    st.session_state[8] = categorias



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


            dfUsoCelular = df[df["UMP_YN"] == "1"]
            dfMediaCelSim = dfUsoCelular["UMP_YN"].astype(int)
            tempoUsoSim = dfMediaCelSim.count()
            dfValid = tabela["VALID_TIME"].astype(int)
            tempoValidoTotal = (dfValid.sum(axis=0))
            tempoValidoTotal = round(tempoValidoTotal, 2)
            percentUso = tempoUsoSim/tempoValidoTotal*10000
            if(percentUso>maxValue):
                maxValue=percentUso

            line=str(i)+","+str(codigo)+","+str(int(percentUso))+"\n"
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
            s['properties']['frequencia'] = int(state_data_indexed.loc[valor,"Pinta"])/100
        else:
            s['properties']['frequencia'] = 0
            
    folium.GeoJsonTooltip(['nome', 'frequencia']).add_to(choropleth.geojson)


    colormap= linear.YlOrRd_09.scale(0,maxValue/100)
    colormap.caption="Frequência de uso do celular por hora"
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
weekdays = (pd.Series.unique(tabela["WEEKDAY"])).astype(str)
weekdays = weekdays.tolist()
weekdays.append("")
weekdays.sort()
usos = ((pd.Series.unique(tabela["ACTION"]))).astype(str)
usos = usos.tolist()
usos.append("")
usos.sort()
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
categorias = (pd.Series.unique(tabela["CATEGORIA"])).astype(str)
categorias = categorias.tolist()
categorias.append("")
categorias.sort()

weekdays=transformaWeekday(weekdays)
usos=traduzVetor(usos)
hCtb=converte(hCtb)

if 8 not in st.session_state:
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    sexoSelec = st.sidebar.radio('Sexo', vsexo)
    categoriaSelec = st.sidebar.radio('Categoria', categorias)
    hCtbSelec = desconverteSing(st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb))
    weekdaySelec = st.sidebar.selectbox('Dia da semana', weekdays)
    usoSelec = voltaTradutor(st.sidebar.selectbox('Tipo de uso', usos))
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    idSelec = st.sidebar.selectbox('Viagem', ids)

else:
    idades = st.session_state[7]
    idadeSelec = st.sidebar.selectbox('Faixa etária do condutor', idades)
    vsexo = st.session_state[2]
    sexoSelec = st.sidebar.radio('Sexo', vsexo)
    categorias = st.session_state[8]
    categoriaSelec = st.sidebar.radio('Categoria', categorias)
    hCtb = st.session_state[3]
    hCtbSelec = desconverteSing(st.sidebar.selectbox('Hierarquia viária (CTB)', hCtb))
    weekdays = st.session_state[4]
    weekdaySelec = st.sidebar.selectbox('Dia da semana', weekdays)
    usos = st.session_state[5]
    usoSelec = voltaTradutor(st.sidebar.selectbox('Tipo de uso', usos))
    drivers = st.session_state[1]
    driverSelec = st.sidebar.selectbox('Condutor', drivers)
    ids = st.session_state[6]
    idSelec = st.sidebar.selectbox('Viagem', ids)

param = []
param.append([0, driverSelec])
param.append([1, weekdaySelec])
param.append([2, usoSelec])
param.append([3, idadeSelec])
param.append([4, sexoSelec])
param.append([5, hCtbSelec])
param.append([6, idSelec])
param.append([7, categoriaSelec])

resul = tabela

for i in param:
    if (i[0] == 0 and (i[1] != "")):
        resul = resul[resul["DRIVER"] == i[1]]
    if (i[0] == 1 and (i[1] != "")):
        resul = resul[resul["WEEKDAY"] == i[1]]
    if (i[0] == 2 and (i[1] != "")):
        resul = resul[resul["ACTION"] == i[1]]
    if (i[0] == 3 and (i[1] != "")):
        resul = resul[resul["IDADE"] == i[1]]
    if (i[0] == 4 and (i[1] != "")):
        resul = resul[resul["SEXO"] == i[1]]
    if (i[0] == 5 and (i[1] != "")):
        resul = resul[resul["HIERARQUIA_CTB"] == i[1]]
    if (i[0] == 6 and (i[1] != "")):
        resul = resul[resul["ID"] == i[1]]
    if (i[0] == 7 and (i[1] != "")):
        resul = resul[resul["CATEGORIA"] == i[1]]

atualizaInfo(resul, param)

if (st.session_state[1] != drivers):
    st.experimental_rerun()
if (st.session_state[2] != vsexo):
    st.experimental_rerun()
if (st.session_state[3] != hCtb):
    st.experimental_rerun()
if (st.session_state[4] != weekdays):
    st.experimental_rerun()
if (st.session_state[5] != usos):
    st.experimental_rerun()
if (st.session_state[6] != ids):
    st.experimental_rerun()
if (st.session_state[7] != idades):
    st.experimental_rerun()
if (st.session_state[8] != categorias):
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
                <h1 style="font-size:32px; text-align:center">Estudo Naturalístico de Direção Brasileiro - Indicadores sobre o uso do celular ao volante</h1>
                <img src='https://www.inf.ufpr.br/lbo21/images/logoBranca.png' id="logoNDS">
            </div>
            <hr>
            """, unsafe_allow_html=True)

##---------------------------------------------


dfUsoCelular = resul[resul["UMP_YN"] == "1"]
dfSemCelular = resul[resul["UMP_YN"] == "0"]

dfValid = resul["VALID_TIME"].astype(int)
tempoValidoTotal = (dfValid.sum(axis=0))
tempoValidoTotal = round(tempoValidoTotal, 2)

dfPick = resul["PICK_UP"].astype(int)
qntPickUp = (dfPick.sum(axis=0))

freqUsoCelular = round((qntPickUp/(tempoValidoTotal/3600)), 2)

dfMediaCelSim = dfUsoCelular["UMP_YN"].astype(int)
dfMediaVelSim = dfUsoCelular["SPD_KMH"].astype(float)
somaVelocidadeSim = dfMediaVelSim.sum(axis=0)
tempoUsoSim = dfMediaCelSim.count()


dfMediaUsoNao = dfSemCelular["UMP_YN"].astype(int)
dfMediaVelNao = dfSemCelular["SPD_KMH"].astype(float)
tempoUsoNao = dfMediaUsoNao.count()
somaVelocidadeNao = dfMediaVelNao.sum(axis=0)

if(tempoUsoSim!=0):
    velDuranteUso = round((somaVelocidadeSim/tempoUsoSim), 2)
else:
    velDuranteUso=0
if(tempoUsoNao!=0):
    velSemUso = round((somaVelocidadeNao/tempoUsoNao), 2)
else:
    velSemUso=0
if(tempoValidoTotal!=0):
    percentUso = round((tempoUsoSim/tempoValidoTotal*100), 2)
else:
    percentUso=0

actions = (pd.Series.unique(resul["ACTION"])).astype(str)
actions.tolist()

col1, col2, col3, col4= st.columns(4)
with col1:
    st.metric("Velocidade média durante o uso (km/h)", velDuranteUso)
with col2:
    st.metric("Velocidade média sem o uso (km/h)", velSemUso)
with col3:
    st.metric("Frequência do uso do celular  (usos/h)", freqUsoCelular)
with col4:
    st.metric(" Percentual do tempo de viagem usando o celular",
              str(percentUso)+"%")
              

slices = []
labels = []
for i in actions:
    if (i != "nan"):
        value = resul[resul["ACTION"] == i]
        value = value["ACTION"].count()
        slices.append(value)
        labels.append(tradutor(i))
data = {"Tipo de uso": labels, "Quantidade de uso": slices}
st.subheader("Distribuição dos tipos de uso do celular (% do tempo)")
fig = px.pie(data, values='Quantidade de uso', names='Tipo de uso',height=300)
st.write(fig)



cidades = ((pd.Series.unique(tabela["CIDADE"]))).astype(str)
cidades = cidades.tolist()
freqCidades = []
cidadesOfc = []

for i in cidades:
    dfPick = resul[resul["CIDADE"] == i]
    dfPick = dfPick["PICK_UP"].astype(int)
    qntPickUp = (dfPick.sum(axis=0))

    dfTime = resul[resul["CIDADE"] == i]
    dfTime = dfTime["VALID_TIME"].astype(int)
    tempoAuxiliar = dfTime.sum(axis=0)
    if (qntPickUp > 0):
        cidadesOfc.append(i)
        freqCidades.append(qntPickUp/(tempoAuxiliar/3600))

data = {"CIDADE": cidadesOfc, "FREQUENCIA": freqCidades}
new_df = pd.DataFrame(data)
dfCidade = new_df.sort_values(["FREQUENCIA"])



bairros = ((pd.Series.unique(tabela["BAIRRO"]))).astype(str)
bairros = bairros.tolist()
freqBairros = []
bairrosOfc = []
for i in bairros:
    dfPick = resul[resul["BAIRRO"] == i]
    dfPick = dfPick["PICK_UP"].astype(int)
    qntPickUp = (dfPick.sum(axis=0))

    dfTime = resul[resul["BAIRRO"] == i]
    dfTime = dfTime["VALID_TIME"].astype(int)
    tempoAuxiliar = dfTime.sum(axis=0)
    if (qntPickUp > 0):
        bairrosOfc.append(i)
        freqBairros.append(qntPickUp/(tempoAuxiliar/3600))

data = {"BAIRRO": bairrosOfc, "FREQUENCIA": freqBairros}

new_df = pd.DataFrame(data)
dfBairro = new_df.sort_values(["FREQUENCIA"])


st.subheader("Frequência de uso do celular por cidade (usos/h)")
bars = alt.Chart(dfCidade).mark_bar(width=20).encode(
    x='FREQUENCIA',
    y=alt.Y("CIDADE",sort='-x') 
)
st.altair_chart(bars)

st.subheader("Frequência de uso do celular por bairro (usos/h)")
bars = alt.Chart(dfBairro).mark_bar(width=20).encode(
    x='FREQUENCIA',
    y=alt.Y("BAIRRO",sort='-x') 
)
st.altair_chart(bars)

corGeral(resul)


st.subheader("Frequência do uso do celular segundo bairro de Curitiba (usos/h)")
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