from __future__ import division
from bs4 import BeautifulSoup
import urllib2,cookielib


def g2crowd(search_term):
    """
    G2 Crowd Webcrawler
    parameters: portion of g2 crowd link between `products/` and `/reviews` in string form
    """
    link, n = search(search_term)
    if n > 0:
        # TODO: handle no reviews
        # n = 30  # number of pages of reviews to crawl
        review_count = 0
        reviews = []
        replace_chars = {'\n': '',
                         ' .': '.',
                         '.': '. ',
                         '[': '',
                         '[': '',
                         ':': '',
                         '/': ' and ',
                         '  ': '',
                         '1.': '',
                         '2.': '',
                         '3.': '',
                         '4.': '',
                         '5.': '',
                         '6.': '',
                         '7.': '',
                         '8.': '',
                         '9.': '',
                         '10.': ''
                         }

        # ---------------------------- PRODUCT 1 ---------------------------- #
        print("Product: " + search_term)

        for i in range(1, n+1):
            site= ("https://www.g2crowd.com"+link+"?page="+str(i))
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  }

            req = urllib2.Request(site, headers=hdr)

            try:
                page = urllib2.urlopen(req)
                content = page.read()
                soup = BeautifulSoup(content, 'html.parser')

                for review in soup.find_all(itemprop='review'):
                    review_count += 1
                    datetime = review.time['datetime']
                    for row in review.find_all('p', attrs={"class" : "formatted-text"}):
                        text = row.text.strip().encode('ascii', 'ignore')  # save and encode text
                        for key, value in replace_chars.iteritems():  # clean text by replacing chars
                            text = text.replace(key, value)
                        if not text.endswith('.'):  # add periods if necessary
                            text = text + '.'
                        reviews.append((text, datetime))  # append review and datetime

            except urllib2.HTTPError:
                print('No reviews exist for %s ' % search_term)
                quit()
    else:
        reviews = []
        review_count = 0
    print("Number of Reviews: " + str(review_count))
    return reviews, review_count


def search(crawl_term):
    """
    Crawls G2 Crowd and returns a list of reviews with their timestamps for any product that contains 'crawl_term' in the product name
    """
    crawl_link = crawl_term.replace(' ', '+')
    site ='https://www.g2crowd.com/search/products?max=10&query=' + crawl_link
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          }
    req = urllib2.Request(site, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print(e)
    content = page.read()
    soup = BeautifulSoup(content, 'html.parser')
    results = soup.find_all('div', {'class':"slat-right"})

    if results:
        for result in results:
            product = result.a.text
            # If the search term is in the product name we have a match
            if crawl_term.lower() in product.lower():
                # Find the review page start link
                review_link = result.a['href']
                # Open review page and find last link
                site = 'https://www.g2crowd.com' + review_link
                hdr = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    }
                req = urllib2.Request(site, headers=hdr)
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError as e:
                    print(e)
                content = page.read()
                soup = BeautifulSoup(content, 'html.parser')
                links = soup.find_all('a', {"class":"pjax"})
                for l in links:
                    text = l.text
                    if 'Last' in text:
                        link = l['href'].split('/')[-1].split('?')[-1]
                        last = [int(part.replace('page=','')) for part in link.split('&') if 'page=' in part][0]
                    else:
                        last = 0
            else:
                # If product not in any of the results, review link and last are null and 0
                review_link = ""
                last = 0
    else:
        # If the search returns nothing, review link and last are null and 0
        review_link = ""
        last = 0
    return review_link, last