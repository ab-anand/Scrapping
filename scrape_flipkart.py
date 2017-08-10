import requests
import os
from bs4 import BeautifulSoup
#os.environ["HTTPS_PROXY"] = "http://username:pass@192.168.1.107:3128"
url= 'https://www.flipkart.com/watches/pr?p%5B%5D=facets.ideal_for%255B%255D%3DMen&p%5B%5D=sort%3Dpopularity&sid=r18&facetOrder%5B%5D=ideal_for&otracker=ch_vn_watches_men_nav_catergorylinks_0_AllBrands'

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
 
source_code = requests.get(url, headers=headers, timeout=15)
plain_text = source_code.text
soup = BeautifulSoup(plain_text,"html.parser")

box  = soup.find('div',{"data-reactid":"331"})

content = box.contents

box_len = len(box)
print(box_len)

for i in range(box_len):
    links = content[i].find('div').find('div').findAll('a')
    print(links[1]['title'])
    
