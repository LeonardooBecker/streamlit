import streamlit as st 
import pandas as pd
import numpy as np

st.write("ALO TEMPO BAO")
st.write("teste firme")

arquivo = open('Dados20220921-134049.csv','r')

teste=arquivo.read()

df = pd.DataFrame(np.random.randn(100,2)+[-25.436129,-49.287566],columns=['lat','lon'])
st.write(df)
cord=[-25.436129,-49.287566]
st.write(cord)
st.map(df)