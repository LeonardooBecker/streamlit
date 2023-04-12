import streamlit as st
import pandas as pd


st.write("Telo")

df = pd.read_csv('AllFullTable.csv', sep=';')

dfUsoCelular = df[df["UMP"] == 1]
dfSemCelular = df[df["UMP"] == 0]

dfMediaCelSim = dfUsoCelular["UMP"].astype(int)
dfMediaVelSim = dfUsoCelular["SPD_KMH"].astype(float)
somaVelocidadeSim = dfMediaVelSim.sum(axis=0)
tempoUsoSim = dfMediaCelSim.sum(axis=0)


dfMediaUsoNao = dfSemCelular["UMP"].astype(int)
dfMediaVelNao = dfSemCelular["SPD_KMH"].astype(float)
tempoUsoNao = dfMediaUsoNao.count()
somaVelocidadeNao = dfMediaVelNao.sum(axis=0)


st.write(somaVelocidadeSim/tempoUsoSim)
st.write(somaVelocidadeNao/tempoUsoNao)

st.write(dfSemCelular)