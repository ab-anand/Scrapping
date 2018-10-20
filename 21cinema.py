from requests_html import HTMLSession
import logging

from lxml import html
from bs4 import BeautifulSoup


'''
http://www.21cineplex.com/theater/bioskop-anggrek-xxi,15,JKTANGG.htm
{
    'name': 'ANGGREK XXI', 
    'jadwal': [
                {
                    'title': 'ALPHA',
                    'time': '12:30 14:40 16:50 19:00 21:10'
                },
                {
                    'title': 'CRAZY RICH ASIANS',
                    'time': '11:45 13:00 14:15 15:30 16:45 18:00 19:15 20:30 21:45'
                },
                {
                    'title': 'PEPPERMINT', 
                    'time': '12:45 14:55 17:05 19:15 21:25'
                }
            ]
}
'''

def detail(url):
    session = HTMLSession()
    
    get_request = session.get(url)

    dict_resutl = {}

    title = get_request.html.xpath('//div[@class="col-m_462"]/div[@class="col-title"]/h2')

    price_element = get_request.html.xpath('//div[@class="col-content"]/table/tr[2]/td[3]')

    harga_bioskop = price_element[0].text

    table_element_div = get_request.html.find('#makan', first=True)

    element_tr = table_element_div.find('tr')

    list_data = []

    parent_dict = {}

    for data in range(1, len(element_tr)):

        value = data

        to_dict = {}

        dk = element_tr[data]

        value = dk.find('a')[1]

        time = dk.find('div')[0]

        to_dict["title"] = value.text
        to_dict["time"] = time.text.replace('\xa0 ', '\n')

        list_data.append(to_dict)

    dict_resutl["name"] = title[0].text
    dict_resutl["info"] = harga_bioskop
    dict_resutl["schedule"] = list_data
    dict_resutl["url"] = url

    print(dict_resutl)

    return dict_resutl



if __name__ == '__main__':
    detail('http://www.21cineplex.com/theater/bioskop-daan-mogot-xxi,194,JKTDAMG.htmTANGG.htm')