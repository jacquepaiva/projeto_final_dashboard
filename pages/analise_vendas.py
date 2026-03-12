import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados():
    # CARREGAR OS DADOS DE VENDAS 
    df= pd.read_csv('dados/vendas.csv')
    df['Data']= pd.to_datetime(df['Data'])
    return df

# UTILIZA A FUNCAO PARA CARREGAR OS DADOS 
# E ARMAZENA EM UMA VARIAVEL PARA USO POSTERIOR
# DATAFRAME DO PANDAS QUE CONTEM OS DADOS DE VENDAS 
dados_vendas= carregar_dados()

st.title(':moneybag: Analise Detalhada de Vendas')

# FILTROS PARA ANALISE
st.sidebar.header("Filtros de Vendas")

