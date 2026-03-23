import streamlit as st
import pandas as pd
import plotly.express as px
from numpy.random import default_rng as rng

st.title("🗺️ Mapa de Vendas por Localização")

dados_mapa = pd.read_csv('dados/vendas_geolocalizacao.csv')

st.sidebar.header("Filtros do Mapa")

opcoes = ["Todas"]

for regiao in dados_mapa["Região"].unique():
    opcoes.append(regiao )
    
    
regioes = st.sidebar.selectbox(
    "Selecione a região",
    options=opcoes,
    index=0
)

opcoes = ["Todas"]

for cat in dados_mapa["Categoria"].unique():
    opcoes.append(cat )
     
categorias = st.sidebar.selectbox(
    "Selecione a categoria",
    options=opcoes,
    index=0
)
opcoes = ["Todas"]

for prod in dados_mapa["Produto"].unique():
    opcoes.append(prod )
produtos = st.sidebar.selectbox(
    "Selecione o produto",
    options=opcoes,
    index=0
)
opcoes = ["Todas"]

for vend in dados_mapa["Vendedor"].unique():
    opcoes.append(vend )
    
vendedores = st.sidebar.selectbox(
    "Selecione o vendedor",
    options=opcoes,
    index=0
)
dados_mapa["Data"] = pd.to_datetime(dados_mapa["Data"])
data_min= dados_mapa["Data"].min().date()
data_max= dados_mapa["Data"].max().date()

data_range = st.sidebar.date_input(
    "Selecione o periodo",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if len(data_range) ==2:
     data_inicio = pd.to_datetime(data_range[0])
     data_fim = pd.to_datetime(data_range[1])
else:
     st.warning("Selecione uma data inicial de um mes e uma final de outro mes no filtro")
     st.stop()

vendas_max = dados_mapa['Vendas'].max()
vendas_min = dados_mapa['Vendas'].min()

faixa_valor = st.sidebar.slider(
    "Faixa de Valor da Venda (R$)",
    vendas_min,vendas_max,
    (157,11997)
)


dados_filtrados = dados_mapa.copy()

if regioes != "Todas":
    dados_filtrados = dados_filtrados[dados_mapa["Região"] == regioes]
    
if categorias!= "Todas":
    dados_filtrados = dados_filtrados[dados_mapa["Categoria"]==categorias]   
    
if produtos!= "Todas":
    dados_filtrados = dados_filtrados[dados_mapa["Produto"]==produtos]
    
if vendedores!= "Todas":
    dados_filtrados = dados_filtrados[dados_mapa["Vendedor"]==vendedores]
    

col1, col2, col3, col4 = st.columns(4)

with col1:
    pontos = len(dados_filtrados)
    st.metric(label="📍Pontos no mapa", value=(pontos))
      
with col2:
    cidades = dados_filtrados['Cidade'].unique()
    total = len(cidades)
    st.metric(label="🏙️ Cidades", value= (total))
    
with col3: 
    receita = dados_filtrados['Vendas'].sum()
    st.metric(label="💰Receita Filtrada", value=(receita))
    
with col4:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label="📈Lucro Filtrado", value= (lucro))
 
 
 
dados_filtrados.rename(columns={'Latitude': 'LATITUDE', 'Longitude':'LONGITUDE'}, inplace=True)
 
dados_filtrados= pd.read_csv("dados/vendas_geolocalizacao.csv",
                             usecols=["LATITUDE", "LONGITUDE"],
                             sep=",", encoding= "utf-8")
dados_filtrados["LATITUDE"]=pd.to_numeric(dados_filtrados["LATITUDE"], errors="coerce")
dados_filtrados["LONGITUDE"]=pd.to_numeric(dados_filtrados["LONGITUDE"], errors="coerce")

st.map(dados_filtrados, latitude='LATITUDE', longitude='LONGITUDE')
 
#cidade = st.dataframe(dados_filtrados) 
#st.header("Resumo por Cidade")
