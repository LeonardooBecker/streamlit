# Autor: Leonardo Becker de Oliveira
# Contato: leonardobecker79@gmail.com
# Link para o repositório: https://github.com/LeonardooBecker/streamlit

import pandas as pd
import streamlit as st
from alteraNomes import *


# Para cada chave presente no dicionário verifica se o valor não é vazio para poder filtrar a tabela ( csv principal ) de acordo com o valor correspondente a chave
def atualizaTabela(dicionario,tabela):
    novaTabela=tabela
    for chave in dicionario:
        if(dicionario[chave]!=""):
            novaTabela = novaTabela[novaTabela[chave]==dicionario[chave]]
    return novaTabela

# Atualiza o dicionário para deixar de acordo com o valor encontrado em session_state
def atualizaDicionario(dicionario):
    for chave in dicionario:
        chaveSelect=chave+"SELECT"
        dicionario[chave]=st.session_state[chaveSelect]
        return dicionario

# Preenche os vetores de filtro de acordo com os dados presentes na tabela e os presentes no dicionário.
def preencheVetorFiltro(dicionario,tabela):
    dicionario=atualizaDicionario(dicionario)
    tabelaAtual = atualizaTabela(dicionario,tabela)
    for chave in dicionario:
        vetorAuxiliar=[]
        vetorAuxiliar = (pd.Series.unique(tabelaAtual[chave])).astype(str).tolist()
        if (dicionario[chave] == ""):
            vetorAuxiliar.append("")
        vetorAuxiliar.sort()
        if(chave=="HIERARQUIA_CTB"):
            vetorAuxiliar=sorted(converte(vetorAuxiliar))
        st.session_state[chave] = vetorAuxiliar