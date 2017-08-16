#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

url = "https://seors.unfccc.int/seors/reports/archive.html"
driver = webdriver.Firefox()
driver.get(url)
time.sleep(5)

# UN Climate Change Conference November 2016 (COP 22/CMP 12/CMA 1) option of dropdown
element = driver.find_element_by_xpath("//*[@value='COP22']")

# click on that dropdown option
element.click()
time.sleep(2)

# click the refresh button
refresh = driver.find_element_by_name("Submit")
refresh.click()
time.sleep(3)

# scrap the source-code of the page obtained
html = driver.execute_script("return document.documentElement.outerHTML")
sel_soup = BeautifulSoup(html, 'html.parser')

# print(sel_soup)

# first row, first column scrapping
tds = sel_soup.findAll('td',{"width":"250"})
data = tds[0]
print(data.contents[0].string) # It should return "Launching the Clean Energy Transformation in Marrakech"
# print(data.contents[1])

driver.quit()




