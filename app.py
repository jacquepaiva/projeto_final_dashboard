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

#analise_vendas= st.Page('./pages/analise_vendas.py',\
#                        title='Analise de Vendas',
#                        icon=':moneybag:')

#analise_produtos= st.Page('./pages/analise_produtos.py',
#                          title='Produtos',
#                          icon=':package:')

#sobre= st.Page('./pages/sobre.py',
#               title='Sobre',
#               icon= ':information_source:')

# CONFIGURANDO A NAVEGACAO 

pg = st.navigation(
    [visao_geral
     #'Analises': [analise_vendas, analise_produtos],
     #'Sobre': sobre
    ]
)

pg.run()