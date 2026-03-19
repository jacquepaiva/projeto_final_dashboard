import streamlit as st 

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon=":bar_chart:",
    layout="wide"
)
# DEFININDO AS PAGINAS 

visao_geral= st.Page('./pages/visao_geral.py', 
                     title='Visao Geral',
                     icon='🏠',
                     default=True)

analise_vendas= st.Page('./pages/analise_vendas.py',\
                       title='Analise de Vendas',
                       icon='💰')

analise_produtos= st.Page('./pages/analise_produtos.py',
                          title='Produtos',
                         icon='📦')

analise_produtos_professor= st.Page('./pages/analise_produtos_professor.py',
                          title='Produtos - professor',
                         icon='📦')




sobre= st.Page('./pages/sobre.py',
              title='Sobre',
              icon= 'ℹ️')

# CONFIGURANDO A NAVEGACAO 

pg = st.navigation(
    [visao_geral, 
     analise_vendas, 
     analise_produtos, 
     analise_produtos_professor,
     sobre]
)

pg.run()