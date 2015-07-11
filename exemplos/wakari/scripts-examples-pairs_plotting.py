#Plots of potentially correlated pairs: 
# 
#
from webplot import p
p.use_doc('pairs')
from wakaridata.weather import Weather
import numpy as np

from datetime import datetime

from wakaridata.yahoofinance import Stocks
stocks = Stocks()

#convert date to milliseconds since the epoch
tomilli = (lambda x: int(datetime.strptime(x,'%Y-%m-%d').strftime('%s'))*1000)

def pairs_plot(st1,st2,length):
    
    adapter1 = stocks[st1][:length]
    adapter2 = stocks[st2][:length]
    
    dates =[tomilli(x) for x in adapter1['Date'][:]] 
    
    #plot the opening price of two stocks
    p.figure()
    p.plot(dates,adapter1['Open'][:],width=500, height=300,title=st1+' vs. '+ st2)
    p.plot(dates,adapter2['Open'][:],width=500, height=300)


#Pepsi and Coke
pairs_plot('pep','coke',500)

#Targe and Wal-Mart
pairs_plot('wmt','tgt',500)

#Dell and Hewlett Packard
pairs_plot('dell','hpq',500)
