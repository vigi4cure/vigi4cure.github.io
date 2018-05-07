#!/usr/bin/python3

import requests, re

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

strava = 'https://www.strava.com/'
session = requests.Session()
#get authenticity_token
r = session.get(strava + 'login')
authenticity_token = find_between(str(r.content), 'name="authenticity_token" value="', '" />')
print(authenticity_token)

payload = {"utf8": "✓", 
           "authenticity_token": authenticity_token,
           "plan": "",
           "email": "wenyibing@gmail.com",
           "password": "wyyzlqm0"}
r = session.post(strava + 'session', data=payload)
print(r)

keywords = 'Brossard'
seg_list = open('segments_%s.csv'%keywords, 'w')
seg_list.write('Segment Id\n')
i = 1
while True:
    url = strava + 'segments/search?utf8=✓&filter_type=cycling&keywords=%s&min-cat=0&max-cat=5&terrain=all&page=%d' % (keywords, i) 
    r = session.get(url)
    print(r)
    b = re.findall('href="/segments/[0-9]+',r.content.decode("utf-8"))
    c = [ x.replace('href="/segments/', '') for x in b]
    print(str(i) + ':' + str(len(c)))
    if len(c) < 2:
        break;
    seg_list.write('\n'.join(c) + '\n')
    i += 1
seg_list.close()
