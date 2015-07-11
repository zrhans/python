#NOAA GLOBAL SUMMARY OF DAY (GSOD) EXAMPLE
#
#Plot two st
from webplot import p
p.use_doc('weather')
from wakaridata.weather import Weather
import numpy as np

from datetime import datetime

weather = Weather()
# Get list of dataset keys
keys = weather.keys()
# Get IOPro text adapter

#sampleList = ['weather/gsod/'+str(i)+'/279470-99999-'+str(i)+'.op' for i in range(2000,2010)]
stat_1 = 'weather/gsod/2008/085750-99999-2008.op'
stat_2 = 'weather/gsod/2008/279470-99999-2008.op'

#function to 
tomilli = (lambda x: int(datetime.strptime(str(x),'%Y%m%d').strftime('%s'))*1000)

adapter = weather[stat_1]
date_1 = adapter[:]['YEARMODA']
date_1 = np.array([tomilli(x) for x in adapter[:]['YEARMODA']])
temp_1 = adapter[:]['TEMP']

adapter = weather[stat_2]
date_2 = adapter[:]['YEARMODA']
date_2 = np.array([tomilli(x) for x in adapter[:]['YEARMODA']])
temp_2 = adapter[:]['TEMP']

source = p.make_source(date=date_1, temp_1=temp_1, temp_2=temp_2)
p.plot_dates('date', 'temp_1', data_source=source,width=500, height=300,title='Daily Average Temperatures STN: 085750')
p.figure()
p.plot_dates('date', 'temp_2', data_source=source,width=500, height=300,title='Daily Average Temperatures STN: 279470')
p.table(source, ['date', 'temp_1', 'temp_2'])

stat_1_1981 = 'weather/gsod/1981/085750-99999-1981.op'

adapter = weather[stat_1_1981]
temp_1_1981 = adapter[:]['TEMP']
p.figure()
p.plot_dates(date_1,temp_1,width=500, height=300,title='Daily Average Temperatures for years 2008 and 1981')
p.plot_dates(date_1,temp_1_1981,width=500, height=300)

