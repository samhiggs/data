import csv
import pandas as pd
from pprint import pprint

#Takes in a csv of product data and converts it to a dictionary.
#key: name
#value: (type, [tags]); tags are separated by a semi-colon
df = pd.read_csv('data/product-export.csv', usecols=['name', 'type', 'tags'])
productDict = df.set_index('name').T.to_dict('list')
# pprint(productDict)

#Take in Processed Data and store all purchases.
processedData = pd.read_csv('data/ProcessedData.csv')
purchases = []
for index, row in processedData.iterrows():
    purchases.append(row['Details'])


#tokenize each product in purchase and store in a list
#then separate quantity into a tuple 
purchasesSplit = []
max_len = 0
max_purchase = []
for p in purchases:
    tokenized = []
    lines = p.split(' + ')
    if len(lines) > max_len:
        max_len = len(lines)
        max_purchase = lines
    for l in lines:
        units = l.split(' X ')
        # print(units)
        tokenized.append(units)
    purchasesSplit.append(tokenized)
#Print out a snapshot of tokenized data
# for sp in tokenized[:10]:
#     print(sp[1])
failures = 0
successes = 0
purchaseData = []
for purchase in purchasesSplit:
    purchaseData.append(len(purchase))
    for item in purchase:
        if len(item) < 2:
            # print(item)
            purchases.append((1, item[0], 'Not Found'))
        elif item[1] in productDict:
            purchaseData.append((item[0], item[1], productDict[item[1]]))
            successes += 1
        else:
            failures+=1
            purchaseData.append((item[0], item[1], 'Not Found'))

# print('There were: {} failures and {} successes and max items is {} {}'.format(failures, successes, max_len, max_purchase))
    # for p in purchaseData:
    #     print(p)


#Convert it into a dataframe
for p in purchaseData[:50]:
    print(p)
#Output columns to CSV: Date, Quantity, Total, datails as [n_items, (first_item_quantity, first_item_name, first_item_type), (second_item_quantity, second_item_name, second_item_type), ...], time, maximum, rainfall amount (millimetres)]

#Take a snapshot of the data
# for p in purchases[:10]:
#     print(p)

