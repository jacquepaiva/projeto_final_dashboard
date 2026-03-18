import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Análise de Produtos - Professor")

# todos os dados de vendas estao armazenados nesta variavel 

dados_vendas = pd.read_csv('dados/vendas.csv')


# TODO: melhorar as opcoes do selectbox para mostrar os produtos disponiveis no dataframe
# Armazena na memoria do computador a opcao selecionada pelo usuario 
option = st.selectbox(
    "Selecione um produto:",
    ("Headphone", "Headset", "Memoria RAM", "Mouse", "SSD", "Teclado", "Webcam"),
)
# quero filtrar os dados de vendas usando a opcao selecionada pelo usuario 
dados_filtrados = dados_vendas[dados_vendas['Produto']== option]

#utilizado o table para debugar o codigo 
#st.table(dados_filtrados.head(10))

col1, col2, col3, col4 = st.columns(4)

with col1:
    receita = dados_filtrados['Vendas'].sum()
    st.metric(label="Receita", value= f'R$ {receita:,.2f}')
      
with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label="Lucro", value= f'R$ {lucro:,.2f}')
    
with col3: 
    qtd = dados_filtrados['Quantidade'].sum()
    st.metric(label="Qtd. Vendida", value= f'{qtd} unidades')
    
with col4:
    preco_medio = receita / qtd 
    st.metric(label="Preco Medio", value= f'R$ {preco_medio:,.2f}')
    

    
    
   
    
