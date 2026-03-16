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

st.title(":moneybag: Analise Detalhada de Vendas")

# FILTROS PARA ANALISE
st.sidebar.header("Filtros de Vendas")

regioes = st.sidebar.multiselect(
    "Selecione as regioes",
    options=dados_vendas["Regiao"].unique(),
    default=dados_vendas["Regiao"].unique()
)
categorias = st.sidebar.multiselect(
    "Selecione as categorias",
    options=dados_vendas["Categoria"].unique(),
    default=dados_vendas["Categoria"].unique()
)
#Recupera as datas minimas e maximas do dataframe para configurar o filtro de data 
data_min= dados_vendas["Data"].min().date()
data_max= dados_vendas["Data"].max().date()
#Filtro de periodo
#O filtro de data e configurado para permitir a selecao de um intervalo
#entre a data minima e maxima presente nos dados
data_range = st.sidebar.date_input(
    "Selecione o periodo",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)
#Garantir que existem duas datas selecionadas 
if len(data_range) ==2:
     data_inicio = pd.to_datetime(data_range[0])
     data_fim = pd.to_datetime(data_range[1])
else:
     st.warning("Selecione uma data inicial e uma final no filtro")
     st.stop()

#Aplicando os filtros selecionados pelo usuario para criar um dataframe filtrado 
dados_filtrados= dados_vendas[
    (dados_vendas["Regiao"].isin(regioes))&
    (dados_vendas["Categoria"].isin(categorias)) &
        (dados_vendas["Data"].between
    (           pd.to_datetime(data_range[0]), 
                pd.to_datetime(data_range[1])))
]
#Metricas filtradas
col1, col2, col3= st.columns(3)
col1.metric("Receita Filtrada", f"R$ {dados_filtrados['Vendas'].sum():,.0f}")
col2.metric("Lucro Filtrado", f"R$ {dados_filtrados['Lucro'].sum():,.0f}")
#Calcula a margem media como a soma do lucro dividido pela soma das vendas, multiplicado por 100 para obter a porcentagem

margem_media= 'NA'
if dados_filtrados['Vendas'].sum() > 0:
    margem_media= (dados_filtrados['Lucro'].sum() / dados_filtrados['Vendas'].sum() * 100)

col3.metric("Margem media", f"{margem_media}%")

# Vendas por vendedor 
# A analise de performance por vendedor e realizada agrupando os dados filtrados pelo nome do vendedor
# E calculando as seguintes metricas:
# - Receita: soma das vendas para cada vendedor 
# - Lucro: soma do lucro para cada vendedor 
# - Transacoes: contagem do numero de vendas para cada vendedor 
# - Ticket medio: media do valor das vendas para cada vendedor
#Os resultados sao arredondados para 2 casas decimais e ordenados pela receita em ordem 
#Decrescente para destacar os vendedores com melhor performance 

st.subheader(":busts_in_silhouette: Performance por vendedor")

vendas_vendedor= dados_filtrados.groupby("Vendedor").agg(
    Receita=("Vendas", "sum"),
    Lucro=("Lucro", "sum"),
    Transacoes=("Vendas", "count"),
    Ticket_Medio=("Vendas", "mean")
).round(2).sort_values(by="Receita", ascending=False)

v_col1, v_col2 = st.columns(2)

with v_col1:
        st.subheader("Tabela")
        st.dataframe(vendas_vendedor, width="stretch")

with v_col2:
    fig= px.bar(
        vendas_vendedor.reset_index(),
        x="Vendedor",
        y="Receita",
        title="Receita e Lucro por Vendedor",
        color="Lucro",
        color_continuous_scale=px.colors.sequential.Purples,
    )
    st.plotly_chart(fig, width='stretch')

#Analise temporal de vendas
st.subheader(":calendar: Analise Temporal")

#Cria uma nova coluna 'Mes' no dataframe filtrado, extraindo o mes e o ano da coluna 'Data'
#A funcao dt.to_period ('M') converte a data para um periodo mensal, e astype(str) converte esse
#periodo para uma string no formato 'YYYY-MM'
#Em seguida, os dados sao agrupados por essa nova coluna 'Mes' para calcular a receita e o lucro total
#de cada mes, resultando em um dataframe mensal que pode ser usado para analise temporal.

dados_filtrados['Mes']= dados_filtrados['Data'].dt.to_period('M').astype(str)
mensal = dados_filtrados.groupby('Mes').agg(
     Receita=('Vendas', 'sum'),
     Lucro=('Lucro', 'sum')
).reset_index()

#Cria um grafico de barras para comparar a receita e o lucro mensal, usando a coluna 'Mes' 
# no eixo x e as colunas 'Receita' e 'Lucro' no eixo y. o parametro barmode='group' e usado para
#exibir as barras de receita e o lucro lado a lado para cada mes, facilitando a comparacao visual entre
#as duas metricas ao longo do tempo. O titulo do grafico e definido como 'Receita x Lucro Mensal'

fig = px.bar(
     mensal, x='Mes', y=['Receita', 'Lucro'],
     barmode='group', title ='Receita x Lucro Mensal')

#O metodo update_layout e usado para ajustar a aparencia do grafico, e o parametro
# xaxis_tickangle=-45 e utilizado para rotacionar os rotulos do eixo x em um angulo de -45 graus,
#o que pode ajudar a melhorar a legibilidade dos rotulos,
#especialmente quando ha muitos meses ou quando os rotulos sao longos. Essa rotacao
#evita que os rotulos se sobreponham e torna o grafico mais facil de interpretar
fig.update_layout(xaxis_tickangle=-45)

#Exibe o grafico usando streamlit, com a largura configurada para se estender ao maximo 
#do conteiner disponivel
st.plotly_chart(fig, width='stretch')


df = dados_filtrados

@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")


csv = convert_for_download(df)


with st.expander(":bar_chart: Dados detalhados"):
    st.write(dados_filtrados)
    st.download_button(
    label="Download CSV",
    data=csv,
    file_name="analise_vendas.csv",
    mime="text/csv",
    icon=":material/download:",
)
    