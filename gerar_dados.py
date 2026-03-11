import pandas as pd 
import numpy as np

np.random.seed(42)
n= 2000
datas = pd.date_range('2023-01-01','2025-12-31', freq='D')
# gerar dados de vendas
dados = pd.DataFrame({
    'Data':np.random.choice(datas, n),
    'Produto':(['Headset','Mouse', 'Teclado', 'Headphone',
                'Webcam', 'SSD', 'Memoria RAM'], n),
    'Categoria':np.random.choice(['Informatica','Armazenamento', 'Perifericos'], n),
    'Regiao': np.random.choice(['Norte', 'Sul', 'Nordeste', 'Sudeste', 'Centro-Oeste'], n),
    'Vendedor':np.random.choice(['Ana Silva', 'Bruno Costa', 'Carla Dias', 'Diego Lima', 'Eva Santos'], n),
    'Vendas':np.random.randint(150, 12000, n)
    'Quantidade':np.random.randint91, 30, n)
    'Custo': np.random.uniform(80, 8000, n)
})