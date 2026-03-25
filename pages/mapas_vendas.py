import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados_geo():
    df = pd.read_csv('dados/vendas_geolocalizacao.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

df = carregar_dados_geo()

st.title("🗺️ Mapa de Vendas por Localização")
st.markdown("Visualize a distribuição geográfica das vendas e aplique filtros para explorar os dados.")

# ── Filtros ──────────────────────────────────────────────────────────────────
st.sidebar.header("Filtros do Mapa")

# Filtro de Região
regioes = ["Todas"] + sorted(df["Região"].unique().tolist())
regiao_sel = st.sidebar.selectbox("Região", regioes)

# Filtro de Categoria
categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
categoria_sel = st.sidebar.selectbox("Categoria", categorias)

# Filtro de Produto
produtos = ["Todos"] + sorted(df["Produto"].unique().tolist())
produto_sel = st.sidebar.selectbox("Produto", produtos)

# Filtro de Vendedor
vendedores = ["Todos"] + sorted(df["Vendedor"].unique().tolist())
vendedor_sel = st.sidebar.selectbox("Vendedor", vendedores)

# Filtro de Período
data_min = df["Data"].min().date()
data_max = df["Data"].max().date()
data_inicio, data_fim = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

# Filtro de valor mínimo de venda
venda_min = int(df["Vendas"].min())
venda_max = int(df["Vendas"].max())
faixa_vendas = st.sidebar.slider(
    "Faixa de Valor da Venda (R$)",
    min_value=venda_min,
    max_value=venda_max,
    value=(venda_min, venda_max),
    step=100,
)

# ── Aplicar filtros ───────────────────────────────────────────────────────────
df_filtrado = df.copy()

if regiao_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Região"] == regiao_sel]

if categoria_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria_sel]

if produto_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Produto"] == produto_sel]

if vendedor_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Vendedor"] == vendedor_sel]

df_filtrado = df_filtrado[
    (df_filtrado["Data"].dt.date >= data_inicio) &
    (df_filtrado["Data"].dt.date <= data_fim)
]

df_filtrado = df_filtrado[
    (df_filtrado["Vendas"] >= faixa_vendas[0]) &
    (df_filtrado["Vendas"] <= faixa_vendas[1])
]

# ── KPIs do resultado filtrado ────────────────────────────────────────────────
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("📍 Pontos no Mapa", f"{len(df_filtrado)}")
col2.metric("🏙️ Cidades", f"{df_filtrado['Cidade'].nunique()}")
col3.metric("💰 Receita Filtrada", f"R$ {df_filtrado['Vendas'].sum():,.2f}")
col4.metric("📈 Lucro Filtrado", f"R$ {df_filtrado['Lucro'].sum():,.2f}")

st.divider()

# ── Mapa ──────────────────────────────────────────────────────────────────────
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Tente ampliar os critérios.")
else:
    # st.map espera colunas chamadas 'latitude' e 'longitude' (minúsculas)
    mapa_df = df_filtrado.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})

    st.subheader("Distribuição Geográfica das Transações")
    st.map(mapa_df[["latitude", "longitude"]], size=500, color="#e63946")

    # ── Tabela de resumo por cidade ───────────────────────────────────────────
    st.divider()
    st.subheader("Resumo por Cidade")

    resumo_cidade = (
        df_filtrado.groupby(["Cidade", "Região"])
        .agg(
            Transações=("Vendas", "count"),
            Receita=("Vendas", "sum"),
            Lucro=("Lucro", "sum"),
        )
        .reset_index()
        .sort_values("Receita", ascending=False)
    )
    resumo_cidade["Receita"] = resumo_cidade["Receita"].map("R$ {:,.2f}".format)
    resumo_cidade["Lucro"] = resumo_cidade["Lucro"].map("R$ {:,.2f}".format)

    st.dataframe(resumo_cidade, use_container_width=True, hide_index=True)

