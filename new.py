#!/usr/bin/python3
import os
#os.environ["HTTPS_PROXY"] = "http://ipg_2015003:abhi%4098@192.168.1.107:3128"
import requests
from bs4 import BeautifulSoup

url='http://www.transindiatravels.com/india/best-places-to-visit-in-india/'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
 
source_code = requests.get(url, headers=headers, timeout=5)
plain_text = source_code.content
soup = BeautifulSoup(plain_text,"html.parser")
link = soup.find('div',{'class':'post-inner'})
h2s = link.findAll('h2')
print(len(h2s))
