"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

# Calcula o tempo válido de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaTempoValido(tabela):
    dfValid=tabela["VALID_TIME"].astype(int)
    return (dfValid.sum(axis=0))

# Calcula a frequência de uso do celular por hora de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaFreqUsoCelular(tabela, tempoValido):
    dfPick=tabela["PICK_UP"].astype(int)
    qntPickUp=(dfPick.sum(axis=0))
    return round((qntPickUp/(tempoValido/3600)),2)

# Calcula o percentual de tempo sem o uso do cinto de segurança de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaPercentWSB(tabela, tempoValido):
    dfWsb=tabela["WSB"].astype(int)
    qntWsb=(dfWsb.sum(axis=0))
    if(tempoValido>0):
        return round(((1-qntWsb/tempoValido)*100),2)
    return 0

# Calcula o percentual de tempo sob excesso de velocidade de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaPercentualExcessoCorrigido(tabela):
    dfVelocidade=tabela["SPD_KMH"]
    dfLimite=tabela["LIMITE_VEL"]

    dfExcesso=tabela[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    tempoExcesso=len(dfExcesso)

    dfCorrigido=tabela[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
    tempoCorrigido=len(dfCorrigido)

    if(tempoCorrigido!=0):
        return round((tempoExcesso/tempoCorrigido*100),2)
    else:
        return 0

def calculaOportunidadeExcesso(tabela,tempoValido):
    dfVelocidade=tabela["SPD_KMH"]
    dfLimite=tabela["LIMITE_VEL"]
    tempoValido=calculaTempoValido(tabela)
    dfCorrigido=tabela[(dfVelocidade>=(dfLimite-10)) & (dfLimite!=0)]
    tempoOportunidade=len(dfCorrigido)
    if(tempoValido!=0):
        return round((tempoOportunidade/tempoValido*100),2)
    else:
        return 0
    

# Calcula o percentual de tempo sob excesso de velocidade de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaPercentualExcesso(tabela,tempoValido):
    dfVelocidade=tabela["SPD_KMH"]
    dfLimite=tabela["LIMITE_VEL"]

    dfExcesso=tabela[(dfVelocidade>=dfLimite) & (dfLimite!=0)]
    tempoExcesso=len(dfExcesso)

    if(tempoExcesso!=0):
        return round((tempoExcesso/tempoValido*100),2)
    else:
        return 0



# Calcula o percentual de tempo usando o celular de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaPercentualUsoCelular(tabela,tempoValido):
    dfUsoCelular = tabela[tabela["UMP_YN"] == "1"]
    dfMediaCelSim = dfUsoCelular["UMP_YN"].astype(int)
    tempoUsoSim = dfMediaCelSim.count()
    if(tempoValido!=0):
        return round((tempoUsoSim/tempoValido*100), 2)
    else:
        return 0

# Calcula a velocidade média durante o uso do celular de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaVelocidadeUsoCelular(tabela):
    dfUsoCelular = tabela[tabela["UMP_YN"] == "1"]
    dfMediaVelSim = dfUsoCelular["SPD_KMH"].astype(float)
    somaVelocidadeSim = dfMediaVelSim.sum(axis=0)
    dfMediaCelSim = dfUsoCelular["UMP_YN"].astype(int)
    tempoUsoSim = dfMediaCelSim.count()
    if(tempoUsoSim!=0):
        return round((somaVelocidadeSim/tempoUsoSim), 2)
    else:
        return 0

# Calcula a velocidade média sem o uso do celular de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaVelocidadeSemUsoCelular(tabela):
    dfSemCelular = tabela[tabela["UMP_YN"] == "0"]
    dfMediaVelNao = dfSemCelular["SPD_KMH"].astype(float)
    somaVelocidadeNao = dfMediaVelNao.sum(axis=0)
    dfMediaUsoNao = dfSemCelular["UMP_YN"].astype(int)
    tempoUsoNao = dfMediaUsoNao.count()
    if(tempoUsoNao!=0):
        return round((somaVelocidadeNao/tempoUsoNao), 2)
    else:
        return 0

# Calcula a velocidade média com o uso do cinto de segurança de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaVMusoCinto(tabela):
    dfUsoCinto = tabela[tabela["WSB"]==1]
    vmUsoCinto=round(((dfUsoCinto["SPD_KMH"].sum(axis=0))/len(dfUsoCinto)),2)
    return vmUsoCinto

# Calcula a velocidade média sem o uso do cinto de segurança de acordo com a tabela fornecida baseada nos filtros selecionados
def calculaVMsemCinto(tabela):
    dfSemCinto = tabela[tabela["WSB"]==0]
    vmSemCinto=round(((dfSemCinto["SPD_KMH"].sum(axis=0))/len(dfSemCinto)),2)
    return vmSemCinto