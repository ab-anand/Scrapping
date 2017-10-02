# ------------- Crawl Stackoverflow and pull relevant data on an product -------------- #
from collections import defaultdict
from bs4 import BeautifulSoup
import sys
import urllib2
import json


def crawl(product):
    print "\nBegin crawling.......\n"
    # Crawler link
    new_link = "https://stackoverflow.com/questions/tagged/%s?sort=newest" % (product)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    req1 = urllib2.Request(new_link, headers=hdr)

    # Try to open page
    try:
        page1 = urllib2.urlopen(req1)
    except urllib2.HTTPError, e:
        print (e.fp.read())

    # Read page
    content = page1.read()
    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')


    # Find the number of tagged questions
    post_count = soup.find_all("div", class_="summarycount al")[0].text
    print ("Total posts on %s = %s" % (product, post_count))
    posts = [{"label":product, "posts":int(post_count.replace(',',''))}]
    # Write number of posts to file
    with open("posts.json", 'w') as fp:
        json.dump(posts,fp)
    print "Total post count saved to file (posts.json)"


    # Output top 5 most recent questions
    recent_qs =  soup.find_all("a", class_="question-hyperlink", href=True)
    # Only take top 5 most recent questions
    if len(recent_qs) > 5:
        count = 5
    else:
        count = len(recent_qs)
    recent = defaultdict(list)
    for i in range(len(recent_qs)):
        q = recent_qs[i].text
        l = "https://stackoverflow.com"+recent_qs[i]['href']
        # print q,l
        recent["questions"].append(q)
        recent["links"].append(l)

    with open("recent.json", 'w') as fp:
        json.dump(recent,fp)
    print "Top 5 most recent questions saved to file (recent.json)"

    # Output top 5 highest voted questions
    vote_link = "https://stackoverflow.com/questions/tagged/%s?sort=votes" % (product)

    req2 = urllib2.Request(vote_link, headers=hdr)

    try:
        page2 = urllib2.urlopen(req2)

    except urllib2.HTTPError, e:
        print (e.fp.read())


    # Read page
    content = page2.read()
    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')

    most = defaultdict(list)
    most_qs =  soup.find_all("a", class_="question-hyperlink", href=True)
    # Only take top 5 of the most popular questions
    if len(most_qs) > 5:
        most_count = 5
    else:
        most_count = len(most_qs)
    for i in range(most_count):
        q = most_qs[i].text
        l = "https://stackoverflow.com"+most_qs[i]['href']
        # print q,l
        most["questions"].append(q)
        most["links"].append(l)

    with open("most.json", 'w') as fp:
        json.dump(most,fp)
    print "Top 5 most popular questions saved to file (most.json)"
    print '\n'


# Pass in product name
try:
    product = sys.argv[1]
    crawl(product)
except:
    print "\nNO SEARCH TERM ENTERED, PLEASE PASS IN PRODUCT NAME AS ARGUMENT!\n"