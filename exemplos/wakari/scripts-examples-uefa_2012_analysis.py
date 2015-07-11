from webplot import p
p.use_doc('uefa')
from collections import Counter
import numpy as np

from wakaridata.sportstats import SportStats

sports = SportStats()

uefa_data = sports[sports.keys()[4]][:]

dob_months = [int(dob.split('-')[1]) for dob in uefa_data['DOB']]

mCount = Counter(dob_months)

for c in mCount:
    print c, mCount[c]

months = mCount.keys()
soccer = np.array(mCount.values())

p.plot(months,soccer,width=500, height=300,title='Number of Births per Month for UEFA 2012')

#http://www.cdc.gov/nchs/data/nvsr/nvsr60/nvsr60_01_tables.pdf#I02
#birth rates per month across USA 2009
US_Total_2009 = np.array([337980,316641,347803,337272,345257,346971,368450,359554\
                          ,361922,347625,320195,340995],dtype='float64')
                
p.figure()
p.plot(months,US_Total_2009,width=500, height=300,title='Totals Births per Month 2009 (USA)')

p.figure()
soccer_normed = soccer/float(soccer.max())
US_normed = US_Total_2009/float(US_Total_2009.max())+.2

p.hold('on')
p.plot(months,US_normed,width=500, height=300,color='red',title='Normalized Birthrates per Month<br/>Red: USA (2009 shifted .2), Blue: NBA')
p.plot(months,soccer_normed,color='blue')
