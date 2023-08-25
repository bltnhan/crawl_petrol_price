from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import xlwings as xw
import pandas as pd

url = 'https://www.pvoil.com.vn/truyen-thong/tin-gia-xang-dau'
service = Service(executable_path=ChromeDriverManager().install())
options = Options()

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
html_content = driver.page_source
with open('html_content.txt', 'w', encoding='utf-8') as f:
    f.write(html_content)
    f.close()
with open('html_content.txt', 'r', encoding='utf-8') as f:
    data_1 = f.read()
    f.close()

pattern = '<option value="(.+)">.+</option>'
time_ = re.findall(pattern,data_1)
print(time_)
df_all = pd.DataFrame()
for t in time_:
    driver.find_element(By.XPATH,f"//select/option[@value='{t}']").click();
    time.sleep(2)
    html_content_item = driver.page_source
    with open('html_content_item.txt', 'w', encoding='utf-8') as f:
        f.write(html_content_item)
        f.close()
    with open('html_content_item.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
#
    pattern_time_update = '<option selected="selected" value="(.+)">.+</option>'
    time_update = re.findall(pattern_time_update,data)

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
    df_all = pd.concat([df,df_all])
df_all.to_excel('Petrol_Price.xlsx')