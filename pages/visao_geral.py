import streamlit as st 
import pandas as pd
import plotly.express as px

def carregar_dados():
    # CARREGAR OS DADOS DE VENDAS 
    df = pd.read_csv('dados/vendas.csv')
    return df

# UTILIZA A FUNCAO PARA CARREGAR OS DADOS 
# E ARMAZENA EM UMA VARIAVEL PARA USO POSTERIOR
# E UM DATAFRAME DO PANDAS QUE CONTEM OS DADOS DE VENDAS  
dados_vendas = carregar_dados()

st.title("Visao geral do negocio")


# KPI'S PRINCIPAIS KEY PERFORMANCE INDICATOR
col1, col2, col3, col4 = st.columns(4)
# COLUNA 1 EXIBE A RECEITA TOTAL, FORMATADA COMO MOEDA BRASILEIRA
col1.metric(":moneybag: Receita Total", f"R$ {dados_vendas['Vendas'].sum():,.2f}")
# COLUNA 2 EXIBE O LUCRO TOTAL, FORMATADO COMO MOEDA BRASILEIRA
col2.metric(":chart_with_upwards_trend: Lucro Total", f"R$ {dados_vendas['Lucro'].sum():,.2f}")
# COLUNA 3 EXIBE O TOTAL DE TRANSACOES QUE E O NUMERO DE LINHAS NO DATAFRAME DE VENDAS 
col3.metric(":shopping_cart: Total transacoes", f"{len(dados_vendas)}")
# COLUNA 4 EXIBE O TICKET MEDIO QUE E A MEDIDA DO VALOR DAS VENDAS,
# FORMATADA COMO MOEDA BRASILEIRA
col4.metric(":bar_chart: Ticket Medio", f"R$ {dados_vendas['Vendas'].mean():,.2f}")

st.divider()

# GRAFICOS DE RESUMOS 

colA, colB = st.columns(2)

with colA:
    # AGRUPAR OS DADOS POR REGIAO E SOMAR AS VENDAS 
    vendas_regiao= dados_vendas.groupby('Regiao')['Vendas'].sum().reset_index()
    fig = px.pie(vendas_regiao, names='Regiao', values='Vendas',
                 title='Distribuição de vendas por região',
                 hole=0.4)
    # EXIBIR O GRAFICO USANDO O STREAMLIT 
    st.plotly_chart(fig, width='stretch')

with colB:
    dados_vendas['Data']= pd.to_datetime(dados_vendas['Data'])
    dados_vendas['Mes']= dados_vendas['Data'].dt.to_period('M').astype(str)

    vendas_mensal= dados_vendas.groupby('Mes')['Vendas'].sum().reset_index()

    # CRIAR UM GRAFICO DE LINHA PARA MOSTRAR A EVOLUCAO MENSAL DAS VENDAS 
    fig = px.line(vendas_mensal, x='Mes', y='Vendas',
                  title='Evolucao Mensal de Vendas',
                  markers=True)
    # EXIBIR O GRAFICO USANDO O STREAMLIT 
    st.plotly_chart(fig, width='stretch')\
    
# TOP  5 PRODUTOS
st.subheader(":moneybag: Top 5 Produtos por Receita")
# AGRUPAR OS DADOS POR PRODUTO E SOMAR AS VENDAS
# DEPOIS SELECIONAR OS 5 PRODUTOS COM MAIOR RECEITA 
top5_produtos= dados_vendas.groupby('Produto')['Vendas'].sum().nlargest(5).reset_index()

# CRIAR UM GRAFICO DE BARRAS PARA MOSTRAR OS
# TOP 5 PRODUTOS POR RECEITA, COM AS BARRAS COLORIDAS DE ACORDO COM O VALOR DAS VENDAS
# O GRAFICO TEM O TITULO "TOP 5 PRODUTOS", O EIXO X MOSTRA OS NOMES DOS PRODUTOS,
# O EIXO Y MOSTRA O VALOR DAS VENDAS 
fig = px.bar(top5_produtos, x='Produto', y='Vendas',
             title='Top 5 produtos',
             color='Vendas',
             color_continuous_scale='purples')

st.plotly_chart(fig, width='stretch')
