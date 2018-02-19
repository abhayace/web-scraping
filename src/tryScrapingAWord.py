import urllib.request as ulib
from bs4 import BeautifulSoup

import re
with open('urban_dictionary_db_trial.csv', 'a') as file:

            wordURL = 'https://www.urbandictionary.com/define.php?term=x0rcist'
            print(wordURL)
            wordPage = ulib.urlopen(wordURL)
            soup = BeautifulSoup(wordPage, 'html.parser')

            the_word = soup.find('div', attrs={'class': 'def-header'}).find('a', attrs={'class': 'word'}).text
            content_div = soup.find('div', attrs={'id': 'content'})
            meaning = content_div.find('div', attrs={'class': 'meaning'}).text
            meaning = meaning.replace('\n', ' ').replace('\r', '')
            contributor_section = content_div.find('div', attrs={'class': 'contributor'})
            contrib_date_sec = str(contributor_section)
            print('Contrib_sec:' + contrib_date_sec)

            contributor = contributor_section.find('a').text
            print('Contrib:' + contributor)
            start_index = contrib_date_sec.find('</a>')

            the_date = re.search('(\w+\s\d+,\s\d+)\s*<', contrib_date_sec[start_index:]).group(1)
            print('date:' +the_date)
            print('END')

            up_down = content_div.find('div', attrs={'class': 'def-footer'})

            upvotes = up_down.find('a', attrs={'class': 'up'}).find('span', attrs={'class': 'count'}).text
            downvotes = up_down.find('a', attrs={'class': 'down'}).find('span', attrs={'class': 'count'}).text

            line = str(the_word+"|"+meaning + "|" + contrib_date_sec[start_index + 3:len(contrib_date_sec) - 6] + "|" + contributor+"|"+upvotes+"|"+downvotes)
            file.write(line)
            file.write('\n')

            file.close()