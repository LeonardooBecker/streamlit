import streamlit as st 
import pandas as pd
import numpy as np

st.write("ALO TEMPO BAO")
st.write("teste firme")

arquivo = open('Dados20220921-134049.csv','r')

teste=arquivo.read()

df = pd.DataFrame(np.random.randn(100,2)/[50,50]+[-49.287566,-25.436129],columns=['lat','lon'])
st.map(df)