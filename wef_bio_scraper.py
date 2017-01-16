import urllib2
import time
from bs4 import BeautifulSoup as bsoup
from bs4 import BeautifulSoup
from yaml import load, Loader
import requests as rq
import re
import unicodedata

#--------------
# PART 1
#--------------

# World Economic Forum Annual Meeting 2017 Speaker Bios Page
base_url = "https://www.weforum.org/events/world-economic-forum-annual-meeting-2017/speakers"
r = rq.get(base_url)
soup = bsoup(r.text, "lxml")

#get speaker names and links
contents = soup.findAll('a', attrs={"class": "tout__link"}, href=True)

baseLink = "https://www.weforum.org"

names = []
links = []
#bios = []

generalData = []
for c in contents[21:]:
  names.append(c.text) #names
  links.append(baseLink + c['href']) #links
  generalData.append({'name': c.text, 'link': baseLink + c['href']})

# for g in generalData:
#   print g

with open('ppl-links.txt', 'w') as outfile:
  for l in links:
    outfile.write(l + '\n')

#--------------
# PART 2
#--------------

#get bio data for all 473 speakers
peopleData = []
with open('ppl-links.txt', 'r') as file:
  data = file.read().split('\n')
  data.remove(data[len(data)-1])

for d in data:
  r2 = rq.get(d)
  soup2 = bsoup(r2.text, "lxml")

  contents2 = soup2.findAll('div', attrs={"class": "page__sidebar"}) #name & title
  contents3 = soup2.findAll('div', attrs={"class": "page__content"}) #description

  for c2,c3 in zip(contents2,contents3):
    peopleData.append({'nameTitle': c2.text,'bio': c3.text})

#test query
for p in peopleData:
  if 'LinkedIn' in p['nameTitle'] or 'LinkedIn' in p['bio']:
    print p['nameTitle']

