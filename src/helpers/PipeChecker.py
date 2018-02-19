filepath = '/home/abhay/PycharmProjects/Web-Scraping/urban_dictionary_db_final.csv'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       # print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       num = line.count('|')
       if num < 5:
           print(line)