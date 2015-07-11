from webplot import p
from collections import Counter
import numpy as np

from wakaridata.sportstats import SportStats

sports = SportStats()

nhl_data = sports[sports.keys()[1]][:]

dob_months = [int(dob.split('-')[1]) for dob in nhl_data['DOB']]

mCount = Counter(dob_months)

print 'All Hockey Players Birth Dates By Month'
for c in mCount:
    print c, mCount[c]

months = mCount.keys()
NHL = np.array(mCount.values())

#plotting NHL Births per Month
p.plot(months,NHL,title='Number of Births per Month for NHL<br/>Blue: Total NHL, Red: NHL (Canada)')

canada = nhl_data[nhl_data['Nationality']=='Canada']

CanadaMonths = [int(dob.split('-')[1]) for dob in canada['DOB']]
CanadaCount = Counter(CanadaMonths)

canadaNHL = np.array(CanadaCount.values())

#plotting Candian Only Players NHL Births per Month
p.plot(months,canadaNHL,color='red')

print '\nCanada Birth Dates By Month'
for c in CanadaCount:
    print c, CanadaCount[c]


#http://www.cdc.gov/nchs/data/nvsr/nvsr60/nvsr60_01_tables.pdf#I02
#birth rates per month across USA 2009
US_Total_2009 = np.array([337980,316641,347803,337272,345257,346971,368450,359554\
                          ,361922,347625,320195,340995],dtype='float64')
                
p.figure()
p.plot(months,US_Total_2009,title='Totals Births per Month 2009 (USA)')

p.figure()

US_normed = US_Total_2009/float(US_Total_2009.max())+.2
canadaNHL_normed = canadaNHL/float(canadaNHL.max())
NHL_normed = NHL/float(NHL.max())

p.hold('on')
p.plot(months,US_normed,color='red',title='Normalized Birthrates per Month<br/>Red: USA (2009 shifted .2), Black: NHL, Blue: NHL (Canada)')
p.plot(months,canadaNHL_normed,color='blue')
p.plot(months,NHL_normed,color='black')
