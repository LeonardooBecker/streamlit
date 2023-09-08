# Autor: Leonardo Becker de Oliveira
# Contato: leonardobecker79@gmail.com
# Link para o repositório: https://github.com/LeonardooBecker/streamlit

import streamlit as st

def rodape():
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