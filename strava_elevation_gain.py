#!/usr/bin/python3

import re
# import sys
from bs4 import BeautifulSoup
import datetime
import pandas as pd
# import time
import requests

def fetch_data(row,now):
    sport = ''
    friend_name = row['name']
    url = requests.get('http://www.strava.com/athletes/'+str(row['id']))
    soup = BeautifulSoup(url.content, "html.parser")
    tables = soup.findAll('table')
    tablerows = tables[0].findAll('tr')
    for row in tablerows:
        # print(row.find('th').text.strip())
        if row.find('th').text.strip() == 'Cycling':
            sport = "\N{BICYCLE}"
        elif row.find('th').text.strip() == 'Running':
            sport = "\N{RUNNER}"
        if row.find('th').text == 'Elevation Gain':
            elevation_gain_raw = row.find('td').text
            elevation_gain = cleanconvert(elevation_gain_raw)
            break
    print(str(now), ' ', friend_name, ' - ', str(elevation_gain))
    output_string = str(now) + ',' + str(friend_name) + ',' + str(elevation_gain) + ',' + sport
    return(output_string)

def cleanconvert(elevation_gain_raw):
    if re.search(r'm',elevation_gain_raw):
        elevation_gain_raw = elevation_gain_raw[:-1]
        elevation_gain_raw = re.sub("[^\d\.\-]", "", elevation_gain_raw)
        elevation_gain_raw = int(float(elevation_gain_raw))

    elif re.search(r'ft',elevation_gain_raw):
        elevation_gain_raw = elevation_gain_raw[:-2]
        elevation_gain_raw = re.sub("[^\d\.\-]", "", elevation_gain_raw)
        elevation_gain_raw = float(elevation_gain_raw) * 0.3048

    elevation_gain_raw = round(elevation_gain_raw,0)
    return(elevation_gain_raw)

        
def main():
    friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)   
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    outputlist = []
    
    #should try to redo this using apply:
    for index,row in friend_df.iterrows():        
        outputlist.append(fetch_data(row,now))
    
    outfile = 'elevation_gain_' + str(datetime.datetime.now().year) + '.csv'
    with open(outfile, 'a+') as f:
        f.write('\n'.join(outputlist) + '\n')
    print(str(now), '  :  ACTION:    new data added to ', outfile)

if __name__ == "__main__":
  main()
