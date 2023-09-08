# Autor: Leonardo Becker de Oliveira
# Contato: leonardobecker79@gmail.com
# Link para o repositório: https://github.com/LeonardooBecker/streamlit

# Converte os nomes das colunas do csv principal para nomes mais amigáveis para o usuário ( os utilizados na interface lateral )
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

#  Desconverte os nome apresentados no painel lateral para os nomes presentes no csv principal ( Número correspondente a cada hierarquia viária )
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
    
# Transorma os nomes definidos no dicionário em nomes mais amigáveis para o usuário ( os utilizados na interface lateral )
def formataNome(keyName):
    if(keyName=="DRIVER"):
        return "Condutor"
    elif(keyName=="BAIRRO"):
        return "Bairro"
    elif(keyName=="CIDADE"):
        return "Cidade"
    elif(keyName=="IDADE"):
        return "Faixa etária do condutor"
    elif(keyName=="HIERARQUIA_CWB"):
        return "Hierarquia viária (Curitiba)"
    elif(keyName=="HIERARQUIA_CTB"):
        return "Hierarquia viária (CTB)"
    elif(keyName=="ID"):
        return "Viagem"
    else:
        return ""