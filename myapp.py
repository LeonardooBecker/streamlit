import streamlit as st 


st.write("ALO TEMPO BAO")
st.write("teste firme")

arquivo = open('Dados20220921-134049.csv','r')

teste=arquivo.read()

st.write(teste)