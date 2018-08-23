
# coding: utf-8
import pandas as pd

# The path to all the sales data files
salesFiles = ['sales_39832.csv',
'sales_73522.csv',
'sales_40067.csv',
'sales_50466.csv',
'sales_74172.csv',
'sales_88136.csv',
'sales_90146.csv',
'sales_51323.csv',
'sales_43914.csv',
'sales_15816.csv',
'sales_32359.csv',
'sales_31902.csv',
'sales_29597.csv']

# Joining up the sales data into one file
Sales = pd.DataFrame()
count = 0
for filename in salesFiles:
    name = 'data/' + filename
    temp = pd.read_csv(name)
    count += len(temp)
    Sales = Sales.append(temp, ignore_index = True)

# Saving the sales combined sales file if we need it later
Sales.to_csv('data/TotalSales.csv')

# Splitting the time and date up into two columns to merge the Date column with the weather data
Sales['Time'] = Sales['Date'].apply(lambda x: x[11:])
Sales['Date'] = Sales['Date'].apply(lambda x: x[0:10])

# Joining up the temperature datasets from 2017 and 2018
temperature = pd.read_csv('data/2017_tmp_data.csv')
temp = pd.read_csv('data/2018_tmp_data.csv')
temperature = temperature.append(temp, ignore_index = True)

# Joining up the rainfall datasets from 2017 to 2018
rainfall = pd.read_csv('data/Rainfall_2017.csv')
temp = pd.read_csv('data/Rainfall_2018.csv')
rainfall = rainfall.append(temp, ignore_index = True)

# Combining the datasets on rainfall and temperature
weather = temperature.merge(rainfall, on=['Year', 'Month', 'Day'])[['Year', 'Month', 'Day', 'Maximum temperature (Degree C)', 'Rainfall amount (millimetres)']]

# The weather data had 3 columns for 'Year', 'Month' and 'Day' 
# so they were joined into one column 'Date'
weather['Date'] = (weather['Year'].map(str) + '-' 
                   + weather['Month'].apply(lambda x: str(x).zfill(2)) + '-' 
                   + weather['Day'].apply(lambda x: str(x).zfill(2)))

# Joining up the weather data with the sales data
total = pd.merge(Sales.drop(['Customer Name', 'Customer Code', 'Note', 'Discount', 'AccountCodeSale', 'AccountCodePurchase', 'Register', 'User', 'Status', 'Sku', 'Line Type', 'Loyalty', 'Quantity', 'Subtotal', 'Sales Tax', 'Paid'], axis=1)
                , weather.drop(['Year', 'Month', 'Day'], axis=1)
                , on='Date'
                , how = 'inner')

# Each transaction had multiple rows, one for each item, one for the total, 
# one for any discount and an extra row if the payment was made by credit card.
# Also there were many duplicates. This cleans all this up into a single row
# retaining the total price.
idx = total.groupby(['Receipt Number'])['Total'].transform(max) == total['Total']
simplified = total[idx].drop_duplicates(subset = ['Date', 'Receipt Number', 'Total', 'Time'])

# Save the processed data
simplified.to_csv('data/ProcessedData.csv')

