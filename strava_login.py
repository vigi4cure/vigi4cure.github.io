#!/usr/bin/python3

import requests, re

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

session = requests.Session()
#get authenticity_token
r = session.get('https://www.strava.com/login')
authenticity_token = find_between(str(r.content), 'name="authenticity_token" value="', '" />')
print(authenticity_token)

payload = {"utf8": "✓", 
           "authenticity_token": authenticity_token,
           "plan": "",
           "email": "wenyibing@gmail.com",
           "password": "wyyzlqm0"}
r = session.post('https://www.strava.com/session', data=payload)
print(r)
# with open('../../html/t.html', 'w') as f:
    # f.write(r.content.decode("utf-8"))
# print(r.content.decode("utf-8"))

# print(str(r.content))
# r = session.get('https://www.strava.com/athletes/14749152')
# print(r)
# with open('../../html/tt.html', 'w') as f:
    # f.write(r.content.decode("utf-8"))

# r = session.get('http://vgweb/athletes/14749152/profile_sidebar_comparison?hl=en-US')
# print(r)
# with open('../../html/s8s.com.html', 'w') as f:
    # f.write(r.content.decode("utf-8"))

seg_list = open('segments_all.csv', 'w')
seg_list.write('Segment Id\n')
for i in range(1,334):
    r = session.get('https://www.strava.com/segments/search?utf8=✓&filter_type=cycling&keywords=&min-cat=0&max-cat=5&terrain=all&page=' + str(i))
    print(r)
    b = re.findall('href="/segments/[0-9]+',r.content.decode("utf-8"))
    c = [ x.replace('href="/segments/', '') for x in b]
    print(len(c))
    seg_list.write('\n'.join(c))
seg_list.close()


