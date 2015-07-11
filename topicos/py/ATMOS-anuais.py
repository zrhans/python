#!/usr/bin/python

import sys, getopt

# coding: utf-8

# #Analise e Tratamento Basico (Triagem) de dados
# Analises por Hans. 2015
#
# * 2012 (10sec)
# * 2013 (10sec)
# * 2014 (10sec ate 1Min seguinte)
# * 2015 (1Min)
#
# ----

# In[1]:

import numpy as np
import pandas as pd
print(sys.version) # Versao do python - Opcional
print(np.__version__) # VErsao do modulo numpy - Opcional
import matplotlib
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')
import datetime
import time

#Dados local
caminho = './dados/'

def app(ano):
    print("Analisando ano %s" % ano)
    df_dados = pd.read_csv(caminho+'sr311-'+ano+'.csv', index_col=None, parse_dates=['Timestamp'])
    print("Dados "+ano+" Importados OK")
    #removendo a primeira coluna, e ajustando a coluna Timestamp para ser o indice
    del(df_dados['Unnamed: 0'])
    df_dados.set_index('Timestamp', inplace=True)
    # Selecionando apenas algumas colunas de interesse
    df_dados = df_dados[['AirTC', 'RH', 'Rain_mm']]

    print('Gerando Graficos Brutos - '+ano)
    plt.figure(figsize=(16,8))
    plt.subplot(2, 1, 1)
    plt.title('Dados Brutos %s' % ano)
    plt.xlabel=''
    df_dados.AirTC.plot()
    df_dados.RH.plot()

    plt.subplot(2, 1, 2)
    plt.ylabel('Chuva - mm')
    plt.xlabel='Data'
    df_dados.Rain_mm.plot()
    #plt.savefig('figs/raw-'+ano+'-rain.png')
    plt.savefig('figs/raw-'+ano+'.png')
    sys.exit()
    # Criando um novo dominio continuo com base no inicio e fim da serie de dados original
    d = pd.DataFrame(index=pd.date_range(pd.datetime(int(ano),1,1), pd.datetime(int(ano),12,31), freq='10s'))
    print("Indice criado OK")
    # Unindo os dois DataFrames pela esquerda (o que nÃ£o houver em d serÃ¡ substituÃ­do por NaN
    ndf_dados = d.join(df_dados)
    #ndf_dados.fillna(0) #Substitui valor NaN por 0
    print("Junção OK")
    print('Gerando Graficos Brutos Reindexados - %s' % ano)
    plt.figure(figsize=(16,8))
    plt.title('Dados Brutos %s' % ano)
    plt.ylabel('Temperatura - Umidade')
    ndf_dados.AirTC.plot()
    ndf_dados.RH.plot()
    plt.savefig('figs/brutos-%s.png' % ano)
    plt.figure(figsize=(16,8))
    plt.ylabel('Chuva')
    ndf_dados.Rain_mm.plot()
    plt.savefig('figs/brutos-chuva-%s.png' % ano)
    #Exportando para um novo arquivo
    df_dados.to_csv('sao_roque_%s-AirTC-RH-Rain.csv' % ano)

    # ###Analises Diarias
    df_dados_diarios = df_dados[['AirTC','RH']].resample('D', how='mean')
    chuva = df_dados.Rain_mm.resample('D', how='sum')
    df_dados_diarios['Acum_Chuva'] = chuva
    # Mostrando Medias diarias
    print('Gerando Graficos Media Diaria - %s' % ano)
    plt.figure(figsize=(16,8))
    plt.subplot(2,1,1)
    plt.title('Media Diaria %s' % ano)
    plt.legend=True
    df_dados_diarios.AirTC.plot(label="Temp")
    df_dados_diarios.RH.plot(label="RH")
    df_dados_diarios.Acum_Chuva.plot(label="ChuvaAcum")
    print('Gerando Graficos Acumulado de Chuva - %s' % ano)
    plt.subplot(2,1,2)
    somado = df_dados_diarios.Acum_Chuva.cumsum()
    somado.plot(label='Acum  %s' % ano)
    plt.savefig('figs/AcumChuva- %s.png' % ano)
    
    # Histograma do Acumulado Diario
    print('Gerando Graficos Histograma Acumulado diario de Chuva - %s' % ano)
    plt.figure(figsize=(16,8))
    df_dados_diarios.Acum_Chuva.plot(kind='hist', orientation='horizontal', alpha=.8)
    plt.savefig('figs/AcumChuvaHist-%s.png' % ano)

    # ### Quais dias o Acumulado de chuva foi superior a 20mm em ano ?
    # Quais dias o Acumulado de chuva foi superior a 20mm em ano?
    
    print(df_dados_diarios.Acum_Chuva[df_dados_diarios.Acum_Chuva > 20.])
    # Quantos dias o Acumulado de chuva foi superior a 20mm em 2015?
    print(df_dados_diarios.Acum_Chuva[df_dados_diarios.Acum_Chuva > 20.].count())
     
    return

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print('test.py -i <arq_entrada> -o <arq_saida>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <arq_entrada> -o <arq_saida>')
         sys.exit();
      elif opt in ("-i", "--iano"):
         #inputfile = arg
         app(arg)
      elif opt in ("-o", "--ofile"):
         outputfile = arg
    print('Arquivo de Entrada: "', inputfile)
    print('Arquivo de Saida  : "', outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

