import requests
from bs4 import BeautifulSoup

url=raw_input('Enter the Snapdeal url: ')

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
 
source_code = requests.get(url, headers=headers, timeout=5)
plain_text=source_code.text
soup=BeautifulSoup(plain_text,"html.parser")
#Product Name
#print soup
link=soup.find('h1',{'class':'pdp-e-i-head'})
title=link.string
title=str(title).strip()
print 'Product: '+title
#Price
link2=soup.find('span',{'itemprop':'price'})
cost=link2.string
print 'Price: Rs. '+cost
#EMI
try:
  link3=soup.find('span',{'class':'emi-price'})
  emi=link3.string
except:
  emi='Not Available'
print 'EMI Status: '+emi
#Ratings
try:
  link4=soup.find('span',{'class':'avrg-rating'})
  ratings=link4.string
except:
  ratings="No ratings yet."
print "Ratings(out of 5): "+ratings
#No. of ratings
try:
   link5=soup.find('span',{'class':'total-rating showRatingTooltip'})
   reviews=link5.string
except:
    reviews="No ratings yet."
print 'Ratings Available: '+reviews
#Bread-crumbs
crumbs=soup.find('div',{"class":"comp-breadcrumb"}).findAll('span')
x=len(crumbs)
print 'Bread-crumbs:'
for i in range(x):
   if crumbs[i].string!=None:
       print crumbs[i].string,

table=soup.findAll('table',{"class":"product-spec"})
len_table=len(table)
specs={}
print '\n'
for i in range(len_table):
    cols = table[i].find_all('td')
    for j in range(0,len(cols),2):
        specs[cols[j].string]=cols[j+1].string
for k, v in specs.items():
    print (str(k), str('-->'), str(v))


