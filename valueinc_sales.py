import pandas as pd


# file_name = pd.read_csv('file.csv')   <--- format of read_csv function

data = pd.read_csv('transaction2.csv')

data = pd.read_csv('transaction2.csv', sep=';')

data.info()


# CostPerTransaction Column Calculataion
CostPerItem = data['CostPerItem']
NumberOfItemsPurchased = data['NumberOfItemsPurchased']
CostPerTransaction = CostPerItem * NumberOfItemsPurchased

# adding new columns to dataframe
data['CostPerTransaction'] = CostPerTransaction.round(2)

# Sales per Transaction
SellingPricePerItem = data['SellingPricePerItem']
SalesPerTransaction = NumberOfItemsPurchased * SellingPricePerItem
data['SalesPerTransaction'] = SalesPerTransaction.round(2)

# Profit per Transaction
ProfitPerTransaction = SalesPerTransaction - CostPerTransaction
data['ProfitPerTransaction'] = ProfitPerTransaction.round(2)

# Markup
data['Markup'] = round((data['ProfitPerTransaction']) / CostPerTransaction, 2)

#combine date fields
day = data['Day'].astype(str)
year = data['Year'].astype(str)
data['Date'] = data['Month'] + '-' + day + '-' + year

#split keywords in column list
split_data = data['ClientKeywords'].str.split(',', expand=True)
# replace brackets
data['ClientAge'] = split_data[0].str.replace('[', '')
data['ClientType'] = split_data[1]
data['ClientSince'] = split_data[2].str.replace(']', '')

data['ItemDescription'] = data['ItemDescription'].str.title()

#bring in and merge new data file 
seasons = pd.read_csv('value_inc_seasons.csv', sep=';')
data = pd.merge(data, seasons, on = 'Month')

#drop columns - ('axis=1' means 'column' / axis=0 means 'row)
data = data.drop(['ClientKeywords', 'Month', 'Day', 'Year'], axis=1)

#Export to CSV
data.to_csv('ValueInc_Cleansed', index=False)
## 'index=False' bc we chose to not include the 'Index' column, will use UserID instead as unique key