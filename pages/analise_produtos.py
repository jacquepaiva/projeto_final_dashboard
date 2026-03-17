import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados():
    # CARREGAR OS DADOS DE VENDAS 
    df= pd.read_csv('dados/vendas.csv')
    df['Data']= pd.to_datetime(df['Data'])
    return df

dados_produtos= carregar_dados()

st.title("📦 Análise de Produtos")

# SELECT PARA SELECIONAR OS PRODUTOS

produtos = st.selectbox(
    "Selecione um produto:",
    options=dados_produtos["Produto"].unique(),
    index=0
)


#st.write(dados_produtos[dados_produtos['Produto'] == produtos])
# CRIANDO OS DADOS FILTRADOS 

dados_filtrados = dados_produtos[dados_produtos['Produto'] == produtos]

# CRIANDO AS METRICAS 

col1, col2, col3, col4 = st.columns(4)

col1.metric("Receita", f"R$ {dados_filtrados['Vendas'].sum():,.2f}")
col2.metric("Lucro", f"R$ {dados_filtrados['Lucro'].sum():,.2f}")
col3.metric("Quantidade",  int(dados_filtrados['Quantidade'].sum()))

media_custo= 'NA'
if dados_filtrados['Vendas'].sum() > 0:
    media_custo= (dados_filtrados['Custo'].mean())
                  
col4.metric("Preco medio", f"R$ {media_custo:,.2f}")

# CRIANDO OS GRAFICOS 

# BARRA - VENDAS POR REGIAO 

col_a, col_b = st.columns(2)

vendas_regiao= dados_filtrados.groupby("Regiao").agg(
    Vendas=("Vendas", 'sum'),
    Receita=("Vendas", "sum"),
    
).round(2).sort_values(by="Receita", ascending=False)

with col_a:
    fig= px.bar(
        vendas_regiao.reset_index(),
        x="Regiao",
        y="Vendas",
        title="Vendas por regiao",
        color="Vendas",
        color_continuous_scale=px.colors.sequential.Sunset,)
    st.plotly_chart(fig, width='stretch')

# VENDAS POR VENDEDOR 

with col_b:
    vendedor_prod = dados_filtrados.groupby('Vendedor')['Vendas'].sum().reset_index()
    fig= px.pie(vendedor_prod, values='Vendas', names='Vendedor',
                title=f'{produtos}: Vendas por vendedor')
    st.plotly_chart(fig, use_container_width=True)

# GRAFICO DE AREA DE EVOLUCAO MENSAL DAS VENDAS 

dados_filtrados['Mes']= dados_filtrados['Data'].dt.to_period('M').astype(str)
mensal_prod = dados_filtrados.groupby('Mes')['Vendas'].sum().reset_index()
fig = px.area(mensal_prod, x="Mes", y='Vendas',
              title=f'Evolucao mensal de {produtos}')
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)