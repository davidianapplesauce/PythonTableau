import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


json_file = open('loan_data_json.json')
data = json.load(json_file)

loandata = pd.DataFrame(data)

loandata['int.rate'].describe()

#using EXP() to get the annual income
income = np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income.round(2)


length = len(loandata)
fico_cat = []
for x in range(0, length):
    category = loandata['fico'][x]
    if category >= 300 and category < 580:
        cat = 'Poor'
    elif category >= 580 and category < 670:
        cat = 'Fair'
    elif category >= 670 and category < 740:
        cat = 'Good'
    elif category >= 740 and category < 800:
        cat = 'Very Good'
    elif category >= 800:
        cat = 'Excellent'
    else:
        cat = 'Unknown'
    fico_cat.append(cat)

fico_cat = pd.Series(fico_cat)

loandata['fico.category'] = fico_cat

#create new column for low or high interest rate
#dfname.loc[dfname[columnname] condition, newColumnName] = 'value if condition met'
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

# loandata.info()

#number of rows/loans by fico category / bar graphs
catplot = loandata.groupby(['fico.category']).size()
catplot.plot.bar(color = 'orange')
plt.show()

catplot = loandata.groupby(['purpose']).size()
catplot.plot.bar(color = 'magenta')
plt.show()

#scatter plots
xpoint = loandata['dti']
ypoint = loandata['annualincome']
plt.scatter(xpoint, ypoint)
plt.show()

#write to csv
loandata.to_csv('loan_cleansed.csv', index = True)