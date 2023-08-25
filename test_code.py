import os
import re
import xlwings as xw
import pandas as pd

with open('html_content.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    f.close()
pattern_time_update = '<option selected="selected" value="(.+)">.+</option>'
time_update = re.findall(pattern_time_update,data)

pattern = '<option value=".+">(.+)</option>'
time_ = re.findall(pattern,data)


pattern = '<td colspan="2" style="text-align: left;">(.+)</td>'
item = re.findall(pattern,data)

pattern = '<td style="text-align: right;">(.+)</td>'
price_1 = re.findall(pattern,data)

price_update = []
gap = []
for x in range(len(price_1)):
    if x%2==0:
        price_update.append(price_1[x])
    else:
        gap.append(price_1[x])
price_update = [x.replace(".","") for x in price_update]

date_update = []
for i in range(len(price_update)):
    date_update.append(time_update[0])
data = list(zip(date_update,item,price_update,gap))
columns = ['date_update','item', 'price_update', 'gap']
df = pd.DataFrame(data=data,columns=columns)
print(df)
# wb = xw.Book()
# sht = wb.sheets('Sheet1')
# sht.range('A1').value = data