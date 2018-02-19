import re
import urllib.request as ulib
from bs4 import BeautifulSoup

def getNextPageURL(pageURL):
    page = ulib.urlopen(pageURL)
    soup_reference_html = BeautifulSoup(page, 'html.parser')

    newPageURL = ''
    current_page_listItem = soup_reference_html.find('div', attrs={'class': 'pagination-centered'})\
        .find('ul', attrs={'class': 'pagination'}).find('li', attrs = {'class':'current'})
    next_page = current_page_listItem.findNext('li')
    if next_page is not None:
        newPageURL = next_page.find('a').attrs['href']
    return newPageURL


urban_dictionary_mainPage = 'https://www.urbandictionary.com/popular.php?character='
urban_dictionary_base = 'https://www.urbandictionary.com'


with open('urban_dictionary_db.csv', 'a') as file:

    for x in map(chr, range(ord('a'),ord('z') + 1)) :

        pageURL = urban_dictionary_base + '/browse.php?character='+x.upper()
        newPageURL = pageURL
        more_pages_remaining = True
        while more_pages_remaining:
            pageURL = newPageURL


            page = ulib.urlopen(pageURL)
            
            soup = BeautifulSoup(page, 'html.parser')
            allwords = soup.find('div', attrs={'id': 'columnist'}).find('ul',attrs={'class':'no-bullet'})
            for li in allwords.findAll('li'):
                licontents = li.find('a')

                wordURL = urban_dictionary_base + licontents['href']
                print(wordURL)
                wordPage = ulib.urlopen(wordURL)
                soup = BeautifulSoup(wordPage, 'html.parser')

                the_word = soup.find('div', attrs={'class': 'def-header'}).find('a', attrs={'class': 'word'}).text
                content_div = soup.find('div', attrs={'id': 'content'})
                meaning = content_div.find('div', attrs={'class': 'meaning'}).text
                meaning = meaning.replace('\n', ' ').replace('\r', '')
                contributor_section = content_div.find('div', attrs={'class': 'contributor'})
                contrib_date_sec = str(contributor_section)
                contributor = contributor_section.find('a').text
                start_index = contrib_date_sec.find('</a>')

                the_date = re.search('(\w+\s\d+,\s\d+)\s*<', contrib_date_sec[start_index:]).group(1)

                up_down = content_div.find('div', attrs={'class': 'def-footer'})
                upvotes = up_down.find('a', attrs={'class': 'up'}).find('span', attrs={'class': 'count'}).text
                downvotes = up_down.find('a', attrs={'class': 'down'}).find('span', attrs={'class': 'count'}).text

                line = str(the_word+"|"+meaning + "|" + the_date + "|" + contributor+"|"+upvotes+"|"+downvotes)
                file.write(line)
                file.write('\n')

            next_pageURL_suffix = getNextPageURL(pageURL)
            newPageURL = urban_dictionary_base + next_pageURL_suffix
            if len(next_pageURL_suffix) == 0:
                more_pages_remaining = False

            file.flush()

    file.close()




