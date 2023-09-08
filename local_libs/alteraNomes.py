"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

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
    elif(keyName=="SEXO"):
        return "Sexo"
    elif(keyName=="CATEGORIA"):
        return "Categoria"
    elif(keyName=="WEEKDAY"):
        return "Dia da semana"
    elif(keyName=="ACTION"):
        return "Tipo de uso"
    else:
        return ""
    

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

def tradutorEnPt(word):
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

def tradutorPtEn(word):
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
    return sorted(vetorTraduzido)
