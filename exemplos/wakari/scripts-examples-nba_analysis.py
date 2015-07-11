from webplot import p
p.use_doc('nba_analysis')
from collections import Counter
import numpy as np

from wakaridata.sportstats import SportStats

sports = SportStats()

nba_data = sports[sports.keys()[3]][:]

months = [int(dob.split('-')[1]) for dob in nba_data['DOB']]

mCount = Counter(months)

for c in mCount:
    print c, mCount[c]

months = mCount.keys()
nba = np.array(mCount.values())

p.plot(months,nba,title='Number of Births per Month for nba')

#http://www.cdc.gov/nchs/data/nvsr/nvsr60/nvsr60_01_tables.pdf#I02
#birth rates per month across USA 2009
US_Total_2009 = np.array([337980,316641,347803,337272,345257,346971,368450,359554\
                ,361922,347625,320195,340995],dtype='float64')
                
p.figure()
p.plot(months,US_Total_2009,title='Totals Births per Month 2009 (USA)')

p.figure()
nba_normed = nba/float(nba.max())
US_normed = US_Total_2009/float(US_Total_2009.max())+.2

p.hold('on')
p.plot(months,US_normed,color='red',title='Normalized Birthrates per Month<br/>Red: USA (2009 shifted .2), Blue: NBA')
p.plot(months,nba_normed,color='blue')
