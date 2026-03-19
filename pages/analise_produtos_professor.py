import streamlit as st
import pandas as pd
import plotly.express as px
import locale

# Função para formatar valores em reais
 
def format_brl(value):
    # Set the locale to Brazilian Portuguese
    # On some systems, the locale string might be slightly different (e.g., 'pt_BR.UTF-8')
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        # Fallback for systems where 'pt_BR.UTF-8' is not available
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except locale.Error:
            print("Warning: Could not set pt_BR locale. Falling back to simple formatting.")
            return f"R$ {value:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
 
    # Format the value as currency with grouping enabled
    # locale.currency() returns a string like 'R$ 1.234,56'
    formatted_value = locale.currency(value, symbol=True, grouping=True)
    return formatted_value

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
    st.metric(label="Receita", value=format_brl(receita))
      
with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label="Lucro", value= format_brl(lucro))
    
with col3: 
    qtd = dados_filtrados['Quantidade'].sum()
    st.metric(label="Qtd. Vendida", value= f'{qtd} unidades')
    
with col4:
    preco_medio = receita / qtd 
    st.metric(label="Preco Medio", value= format_brl(preco_medio))
    

    
## SEGUNDA PARTE DA AULA 19-03

colA, colB = st.columns(2)

with colA:
    df_agrupado = dados_filtrados.groupby('Regiao')['Vendas'].sum().reset_index()
    # para debugar para ver como fica o filtro se agrupou por regiao
    #st.dataframe(df_agrupado)
    fig = px.bar(
        df_agrupado,
        x='Regiao',
        y='Vendas',
        title=f'Vendas por Regiao - {option}',
        color='Vendas')
    st.plotly_chart(fig, width='stretch')
    
    
with colB:
    df_agrupado_2= dados_filtrados.groupby('Vendedor')['Vendas'].sum().reset_index()
    fig = px.pie(df_agrupado_2, 
                 values= 'Vendas', 
                 names='Vendedor',
                 title=f'Vendas por Vendedor - {option}')
    st.plotly_chart(fig, width='stretch')

# Criando a coluna 'Mes' para analise temporal 
dados_filtrados['Data']= pd.to_datetime(dados_filtrados['Data'])
dados_filtrados['Mes'] = dados_filtrados['Data'].dt.to_period('M').astype(str)   
## DEBUG para ver se criou campo mes st.dataframe(dados_filtrados.head(10))

df_agrupado_3= dados_filtrados.groupby('Mes')['Vendas'].sum().reset_index()
fig = px.area(df_agrupado_3, x='Mes', y='Vendas')
st.plotly_chart(fig, width='stretch')
   
    
