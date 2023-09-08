# Autor: Leonardo Becker de Oliveira
# Contato: leonardobecker79@gmail.com
# Link para o repositório: https://github.com/LeonardooBecker/streamlit

# Calcula o tempo válido de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaTempoValido(tabela):
    dfValid=tabela["VALID_TIME"].astype(int)
    return(dfValid.sum(axis=0))

# Calcula a frequência de uso do celular por hora de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaFreqUsoCelular(tabela, tempoValido):
    dfPick=tabela["PICK_UP"].astype(int)
    qntPickUp=(dfPick.sum(axis=0))
    return round((qntPickUp/(tempoValido/3600)),2)

# Calcula o percentual de tempo sem o uso do cinto de segurança de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaPercentWSB(tabela, tempoValido):
    dfWsb=tabela["WSB"].astype(int)
    qntWsb=(dfWsb.sum(axis=0))
    return round(((1-qntWsb/tempoValido)*100),2)

# Calcula o percentual de tempo sob excesso de velocidade de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaPercentualExcesso(tabela):
    dfVelocidade=tabela["SPD_KMH"]
    dfLimite=tabela["LIMITE_VEL"]

    dfExcesso=tabela[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    tempoExcesso=len(dfExcesso)

    dfCorrigido=tabela[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
    tempoCorrigido=len(dfCorrigido)

    if(tempoCorrigido!=0):
        pcExcesso=round((tempoExcesso/tempoCorrigido*100),2)
    else:
        pcExcesso=0

    return pcExcesso