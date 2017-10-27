import requests
from lxml import html
from collections import defaultdict


 # Pre Stuff
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
teams = ['Manchester City', 'Manchester United', 'Tottenham Hotspur', 'Chelsea', 'Arsenal', 'Watford', 'Newcastle United', 'Burnley', 'Liverpool', 'Southampton', 'Huddersfield Town', 'Brighton and Hove Albion', 'West Bromwich Albion', 'Leicester City', 'Swansea City', 'West Ham United', 'Stoke City', 'Everton', 'Bournemouth', 'Crystal Palace']
teams.sort()
url = 'https://www.premierleague.com/tables'
concat_url = 'https://www.premierleague.com/'


# Get parsed page using lxml
def get_parsed_page(url):
	response = requests.get(url, headers=headers, timeout=10)
	parsed_page = html.fromstring(response.content)
	return parsed_page


# Main 
print(teams)
team = raw_input('Enter Team Name from above list: ')
parsed_page = get_parsed_page(url)

# Getting required details
a_teams = parsed_page.xpath('//tbody[@class="tableBodyContainer"]//td[@class="team"]/a/span[@class="long"]/text()')
points = parsed_page.xpath('//tbody[@class="tableBodyContainer"]//td[@class="points"]/text()')
next_match_link = parsed_page.xpath('//tbody[@class="tableBodyContainer"]//td[@class="nextMatchCol hideMed"]//a/@href')

ref = defaultdict(list)

for i, (a,b,c) in enumerate(zip(a_teams, points, next_match_link)):
	ref[a] = [i+1, a, b, concat_url + c]

print("Current Position: "+str(ref[team][0]))
print("Total Points: "+str(ref[team][2]))
print("Next Match: "+ref[team][3])
