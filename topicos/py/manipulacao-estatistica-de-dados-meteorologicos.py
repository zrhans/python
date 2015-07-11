
# coding: utf-8

# # Manipulação Estatística em dados Meteorologicos
# ----
# - Manipular estruturas de dados 2d (bidimensionais) usando as estruturas Python dos pacote Numpy e PANDAS*.
# - Mineirar, manipular e aplicar tratamento estatístico em séries temporais meteorológicas.
# 
#  \* Pacote para análise de dados - [http://pandas.pydata.org/](http://pandas.pydata.org/)

# # PARTE 01
# Na Parte 01 vamos utilizar uma série temporal de contações diárias de um ativo financeiro
# como fonte de dados para compreender os conceitos (termos) e algumas das funcionalidades das 
# estruturas(objetos) de manipulação de dados. 

# Os principais objetos do PANDAS são:
#     - Series : comporta-se como um array numpy 1d. 
#         - Aceita quisquer tipos de dados
#         - Operações vetorizadas
#         - Sintaxe: s = Series; Ex: s1 = [0,1,2,3,4,5]
#     
#     - DataFrame: comporta-se como uma matriz bidimensional (2d numpy array like)
#         - Aceita quisquer tipos de dados. 
#         - Possui um índice por padrão (1 coluna) que pode ser alterado e/ou reorganizado
#         - As colunas possuem nome
#         - As colunas podem ser movidas e/ou reorganizadas
#         - As colunas podem ser criadas a partir de operações matemáticas (*operations on rows*)
#         - Referências em *prior rows* pelo método .diff()
#         - Relevantes Funções de biblioteca:
#             - Média móvel *rolling means in PANDAS*
#             - Desvio padrão, correlação, covariançia, etc
#             - Gráficos (usa a biblioteca matplotlib - http://matplotlib.org/)
#         - Operações vetorizadas.
#         - Sintaxe: df = DataFrame(data, index=index, columns=list); 
#             Ex: df = DataFrame(np.random.randn(8, 3), index=index, columns=['A', 'B', 'C'])
#     
# * Os objetos Series e Dataframe também pode se comportar como dicionários *dictionary like*
# * Praticamente todos os objetos possuem o método para fatiamento *slicing* para seleção de dados.
#     

# 
# ## Obtendo (mineirando) e preparando a base de dados
# 
# Com finalidade prática, vamos usar uma série histórica, mineirando alguns dados da cotação do 
# ativo CSNA públicos disponíveis na web via yahoo finance e armazenar um conjunto em um arquivo
# do tipo `.csv`
# 

# In[1]:

import pandas as pd
from pandas import DataFrame

import datetime
import pandas.io.data  ## Vamos utilizar para acesso à API do Yahoo finance e importação de dados

import matplotlib.pyplot as plt


# In[2]:


csna3 = pd.io.data.get_data_yahoo('CSNA3.SA',
                                  start = datetime.datetime(2000,10,1),
                                  end = datetime.datetime(2015,7,10))

# o Método .head() mostra as primeiras linhas do objeto
csna3.head()


# **Resultado da chamada ao método `.head()` via comando `csna3.head()`**
# 
# <pre>
# 	Open	High	Low	Close	Volume	Adj Close
# Date						
# 2000-10-02	19.50000	19.50000	19.00001	19.28333	7034400	481.03537
# 2000-10-03	19.66332	19.83334	19.17334	19.17334	16718400	478.29154
# 2000-10-04	19.49333	19.49333	19.10666	19.23334	7365600	479.78828
# 2000-10-05	19.23334	19.23334	19.23334	19.23334	0	479.78828
# 2000-10-06	19.36668	19.36668	19.13333	19.21668	3924000	479.37280
# </pre>

# In[3]:

# Salvar o dados do DataFrame para o formato .csv
csna3.to_csv('csna3_ohlc.csv')


# A partir desse momento, não precisamos mais importar os dados do *yahoo finance*.
# Carregaremos os dados diretamente a partir do arquivo csv criado.

# In[4]:

# Lendo o arquivo .csv [pd.read_csv('arquivo.csv')]
# Comente sobre os dois argumentos além do filename
df = pd.read_csv('csna3_ohlc.csv', index_col='Date', parse_dates=True)
df.head()


# ### Operação com colunas

# In[5]:

# Especificando apenas uma coluna (via string '')
df2 = df['Open']
df2.head()


# In[6]:

# Especificando multiplas colunas (via lista[])
df3 = df[['Open', 'Close']]
df3.head()


# In[7]:

# Removendo uma coluna
df3_tmp = df3.copy() # Criando uma cópia de segurança
del df3['Close']
df3.head()


# In[8]:

df3 = df3_tmp.copy() # Restaurando o df3 ao estado anterior
del df3_tmp          # Removendo a cópia de segurança
df3.head()


# In[9]:

df3.head()


# In[10]:

# Renomeando as colunas
df3.rename(columns={'Close': 'CLOSE'}, inplace=True)
df3.head()


# In[11]:

# Filtrando dados via condição lógica `df3[(condição-logica)]`
df4 = df3[(df3['CLOSE'] > 1)] # Seleciona onde valores de CLOSE são > 1
df4.head()


# In[12]:

# Criando colunas com colunas a partir de operações matemáticas
df['H-L'] = df['High'] - df.Low   
df.head()


# Note que usamos duas formas (ambas são aceitas) para nos referir às colunas *High* e *Low* no *DataFrame*:  `df['High']` e `df.Low`

# In[13]:

# Médias móveis (em pandas `pd.rolling_mean()`)
# Criando uma coluna com a Media móvel com janela de 100 períodos
df['100MA'] = pd.rolling_mean(df['Close'], 100) 
print df[200:205]  # Os primeiros 100 valores serão NaN


# In[14]:

# Referências em *prior rows* pelo método .diff()
# Criando uma nova colunas com valores calculados
# de uma coluna ['Close'] menos o valor anterior (por linhas)
df['Diferenca'] = df['Close'].diff()
df.head()


# ### Gráficos

# In[23]:

figure(figsize=(16,8))
# Grafico do DataFrame Inteiro
df.plot()
savefig('img-df-inteiro.png')


# Observa-se que *plotar* um gráfico do DtaFrame inteiro não tem muita serventia, pois algumas informações ficam mascaradas uma vez que todas compartilham o mesmo eixo de imagem (y).

# In[31]:

# Gráfigo de uma coluna específica
# Gráfico da média móvel 100MA
figure(figsize=(16,8))
df['100MA'].plot()
df['hpm'] = 7.02
df['hpm'].plot()
savefig('img-df-hpm-100MA.png')


# In[49]:

# Gráfigo de colunas múltiplas
# Gráfico da média móvel 100MA e Close
figure(figsize=(16,8))
df['100MA'].plot(legend=True)
df['Close'].plot(legend=True)
#df[['Close','100MA']].plot()
savefig('img-df-Close+100MA.png')


# In[50]:

# Gráfigo de colunas múltiplas
# Gráfico da média móvel 100MA e Close
figure(figsize=(16,8))
df[['Open','High','Low','Close','100MA']].plot()
savefig('img-df-ohlc+100MA.png')


# ### Gráficos 3D
# Para traçar gráficos 3D, é necessário a importação de alguns módulos do pacote **mpl_toolkits**. O principal módulo aser importado é o *mplot3d*  via comando `from mpl_toolkits.mplot3d import Axes3D`.

# In[83]:

'''
    Pode-se usar um grágico 3D para mostrar o preço de fechamento 
    (*Close*) do ativo em função do volume de operações e a covariância 
    entre esses dados. Interessante se pudermos usar o mouse para mudar
    a visão. Nos demais casos é melhor um gráfico de espalhamento
    bidimensional.
'''
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(16,10))
graf3d = fig.gca(projection='3d')

#============================================================
#           Recriando o DataFrame com indice inteiro
#
df = pd.read_csv('csna3_ohlc.csv', parse_dates=True)
df['H-L'] = df.High - df.Low
df['100MA'] = pd.rolling_mean(df['Close'], 100) 
df['Diferenca'] = df['Close'].diff()
#============================================================
# df.index é o índice dos dados
graf3d.scatter(df.index, df['H-L'], df['Close'], alpha=0.5) 
# Nomeando os 3 eixos
graf3d.set_xlabel('Index')
graf3d.set_ylabel('H-L')
graf3d.set_zlabel('Close')
fig.show()
savefig('img-df-3d-HLxClose.png')

# Comportamento de H-L responde a variação no Volume
fig = plt.figure(figsize=(16,10))
graf3d =fig.gca(projection='3d')
graf3d.scatter(df.index, df['H-L'], df['Volume'], alpha=0.5) 
# Nomeando os 3 eixos
graf3d.set_xlabel('Index')
graf3d.set_ylabel('H-L')
graf3d.set_zlabel('Volume')
fig.show()
savefig('img-df-3d-HLxVol.png')


# ### Múltipos Gráficos (*subplots*)
# 

# In[3]:

""" Adicionando uma coluna ao DataFrame para adicionar o cálculo do
    valor do Desvio Padrão (*STD*)
    
    .sublot(rows,cols, plot-number)
"""
#============================================================
#         Recriando o DataFrame com indice sendo a Data
#
df = pd.read_csv('csna3_ohlc.csv', index_col='Date', parse_dates=True)
df['H-L'] = df.High - df.Low
df['100MA'] = pd.rolling_mean(df['Close'], 100, min_periods=1) 
df['Diferenca'] = df['Close'].diff()
#============================================================

df['STD'] = pd.rolling_std(df['Close'], 25, min_periods=1)

fig = plt.figure(figsize=(16,10))

# Criando eixos para multiplot
# Superior (Linha 1)
ax1 = plt.subplot(2,1,1)
# ax1.plot(df['Close'])             # usando matplotlib diretamente
df['Close'].plot(legend=True)       # usando pandas

# Inferior (Linha 2)
# se quiser compartilhar o eixo .subplot(2,1,2, sharex = ax1)
ax2 = plt.subplot(2,1,2) 
df['STD'].plot(legend=True)    
fig.show()
savefig('img-df-mpl-close-std.png')


# ### Informações Estatísticas 
# A Descrição Estatística de um DataFrame (Das séries em geral) é obtida pelo método comum `.describe`. 
# 
# O exemplo abaixo permite estimar os mais comuns (principais - [Distribuição Normal e Escalas](https://pt.wikipedia.org/wiki/Estat%C3%ADstica#/media/File:Normal_distribution_and_scales.gif)) parâmetros estatísticos sobre uma série de dados.
# <pre>
# In [76]: series.describe()
# Out[76]: 
# count    500.000000
# mean      -0.039663
# std        1.069371
# min       -3.463789
# 25%       -0.731101
# 50%       -0.058918
# 75%        0.672758
# max        3.120271
# dtype: float64
# </pre>
# Uma coluna de um DataFrame possui o método `.describe()`

# In[4]:

# Já que cada coluna do DataFrame comporta-se como uma série,
# pode-se invocar o método `.describe` em todo o DataFrame

df.describe()


# In[9]:

'''
    Correlação = Relação na variação entre duas grandezas. Quão 
    influente é a variação de uma variável como causa da variação
    da outra. Obs: Correlação não é causa.
    
    Covariância = Medida da força da correlação. Quão forte é a 
    influência de uma sobre a outra.
'''

# Mostrando a correlação
df.corr()


# In[6]:

# Mostrando a Covariância
df.cov()


# In[8]:

# Se quisermos apenas a estatística comparativa entre duas variáveis
df[['Volume', 'H-L']].corr()


# **Exercício 1 - ** *Construa uma tabela das correlações entre vários ativos. Use os dados públicos Yahoo finance para obter as séries históricas e descreva como você observa as correlações entre os ativos de alguns segmentos.*
# 
# **Exercício 2 - ** *Aplique os conceitos (termos) e as funcionalidades das estruturas(objetos) que você aprendeu nessa aula em um conjunto de séries históricas meteorológicas.*
# 
# Fonte de dados para utilizar: http://200.132.24.235/csda/topicos-met.csv.zip

# ----
# ## *Map Functions*
# 
# Vamos refazer algumas operações utilizando *map functions* ao invés dos 
# métodos do pandas. É importante saber como fazer algumas coisas do jeito "difícil" ou como se diz "à unha", pois nem sempre se quer utilizar
# *black boxes* embora tudo no python seja *open source*.
# 
# O Exemplo abaixo ilustra a possibilidade de você criar sua própria função e aplicá-la a cada valor (linha por linha) da coluna de um DataFrame. Esse exemplo é interessante pois a sua função particular pode receber quantos e quais parâmetros você quiser.

# In[17]:

#============================================================
#         Criando o DataFrame com indice sendo a Data
#
df = pd.read_csv('csna3_ohlc.csv', index_col='Date', parse_dates=True)
#============================================================
import random

def function(data):
    '''
        Recebe o parâmetro data como argumento e o retorna multiplicado
        por um numero aleatorio entre 0 e 5
    '''
    x = random.randrange(0,5)
    return data*x



df['Multiple'] = map(function, df['Close'])
df.head()


# In[ ]:



