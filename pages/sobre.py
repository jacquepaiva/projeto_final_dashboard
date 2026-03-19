import streamlit as st
import pandas as pd

st.header("ℹ️ Sobre o Dashboard")
st.subheader("Dashboard de Análise de Vendas")

multi = '''Este dashboard foi desenvolvido como projeto integrador do curso de Streamlit.  
        **Tecnologias utilizadas:**  
        -Streamlit — Framework para apps web em Python  
        -Pandas — Manipulação e análise de dados  
        -Plotly Express — Visualizações interativas  
        -NumPy — Geração de dados numéricos  
        **Funcionalidades:**  
        📊 Visão geral com KPIs e gráficos resumo  
        💰 Análise detalhada de vendas com filtros  
        📦 Análise individual por produto  
        📥 Download de dados filtrados'''
        
st.markdown(multi)