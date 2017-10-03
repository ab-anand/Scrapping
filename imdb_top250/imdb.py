import csv
import requests
from bs4 import BeautifulSoup


def ScrapeData(url):
	"""
	utility function to scrape the ratings webpage ar given url
	"""
	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, 'html5lib')
	table = soup.find('tbody')
	chart = []
	for row in table.findAll('tr'):
		movie={}
		for col in row.findAll('td'):
			if col['class'] == ['titleColumn']:
				data = col.get_text().split('\n')
				movie['rank'] = data[1].strip()[:-1]
				movie['name'] = data[2].strip()
				movie['year'] = data[3].strip()[1:-1]
				movie['info_link'] = col.a['href']
			if col['class'] == ['ratingColumn','imdbRating']:
				movie['rating'] = col.get_text().replace('\n','')
		chart.append(movie)        
	return chart


def CrawlIMDB():
	"""
	function to scrape each category
	"""
	BASE_URL = 'http://www.imdb.com/chart/'
	CATEGORIES = ['top-indian-movies','top','toptv','bottom']
	chartDB = []
	for category in CATEGORIES:
		print("Scraping {} category.".format(category))
		chart = {}
		chart['category'] = category
		url = BASE_URL + category
		chart['table'] = ScrapeData(url)
		chartDB.append(chart)
	return chartDB


def SaveAsCSV(db):
	"""
	utility function to save ratings in a csv file
	"""
	filename = 'ratings/' + db['category'] + '.csv'
	with open(filename, 'w') as f:
		w = csv.DictWriter(f, ['rank', 'name', 'year', 'rating', 'info_link'])
		w.writeheader()
		for movie in db['table']:
			w.writerow(movie)  


def main():
	myDB = CrawlIMDB()
	for db in myDB:
		SaveAsCSV(db)
   
		
if __name__ == "__main__":
	main()
