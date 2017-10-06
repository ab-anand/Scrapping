
#Modules used
import csv
from bs4 import BeautifulSoup
import requests

#Scrape one page to get data of 50 animes
def ScrapePageData(limit):
    anime_list = []
    url = 'https://myanimelist.net/topanime.php?limit=' + str(limit)
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    page = requests.get(url,headers = headers)
    if page.status_code == 200 :
        soup = BeautifulSoup(page.text,'html.parser')
        anime = soup.find_all('tr','ranking-list')
        for item in anime :
            anime = {}
            rank = item.find('td','rank ac')
            anime['rank'] = rank.span.string
            name = item.find('a','hoverinfo_trigger fl-l fs14 fw-b')
            anime['name'] = name.string
            anime['url'] = name['href']
            info = item.find('div','information di-ib mt4')
            details = info.text.split('\n')
            anime['episodes'] = details[1].lstrip()
            anime['date'] = details[2].lstrip()
            anime['members'] = details[3].lstrip()
            rating = item.find('div','js-top-ranking-score-col di-ib al')
            anime['rating'] = rating.span.string
            anime_list.append(anime)
        
        print('Scraped Animes from %s to %s',limit+1,limit+50)
        return anime_list

#Write to csv
def AddtoCSV(anime_list) :
    filename = 'animelist.csv'
    with open(filename,'a') as csvfile :
        fieldnames = ['rank','name','episodes','date','members','rating','url']
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        if anime_list[1]['rank'] == '1' :
            writer.writeheader()
        
        for anime in anime_list:
            writer.writerow(anime)
    
    
        

def main():
    limit = 0
    while True:
        animes = ScrapePageData(limit)
        if animes == None :
            break;
        else :
            AddtoCSV(animes)
        limit += 50
    
    print('Scrapping Complete')


if __name__ == "__main__" :
    main()