import json, os, requests
from bs4 import BeautifulSoup
from selenium import webdriver

os.environ["HTTPS_PROXY"] = "http://ipg_2015003:abhi%4098@192.168.1.107:3128"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'}
 

#url to retrieve
url = 'https://www.coupondunia.in/category/recharges'

#open Firefox and retrieve the url
driver = webdriver.Firefox()
driver.get(url)

#grab the html
html = driver.execute_script('return document.documentElement.outerHTML')
sel_soup = BeautifulSoup(html, 'html.parser')

#getting the data

h3=sel_soup.findAll('h3')
h1=sel_soup.h1.string
h3=h3[0].string

#findind the meta content whose name='description'
content=sel_soup.findAll("meta")
con=content[1]['content']
title=sel_soup.title.string

#saving data to a json file
with open('first_day.json','w', encoding='utf-8') as f:
     f.write(json.dumps({'h1': h1,'Title':title,'h3':h3,'content':con}, ensure_ascii=False))

