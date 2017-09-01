#!/usr/bin/python3
import os
import csv
import pandas as pd

import requests
from bs4 import BeautifulSoup

url='http://www.transindiatravels.com/india/best-places-to-visit-in-india/'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
 
source_code = requests.get(url, headers=headers, timeout=5)
plain_text = source_code.content
soup = BeautifulSoup(plain_text,"html.parser")

h2s = soup.findAll('h2')
data = []
for i in range(len(h2s)):
    a = h2s[i].get_text()
    pos = a.find('. ')
    data.append(a[pos+1:])

df = pd.DataFrame(data)

df.to_csv('dataset.csv', index=False, header=False)
