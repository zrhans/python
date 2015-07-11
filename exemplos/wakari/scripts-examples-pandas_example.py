from webplot import p
import pandas
df = pandas.read_csv('auto-mpg.csv')
p.use_doc('cars')
source = p.model('PandasDataSource', df=df)
source.update()
p.pandastable(source)
p.figure()
p.scatter('mpg', 'weight', data_source=source)
p.figure()
p.scatter('mpg', 'yr', data_source=source)
