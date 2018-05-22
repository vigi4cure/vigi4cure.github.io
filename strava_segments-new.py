#!/usr/bin/python3

import re
import sys
import csv
import time
import datetime
import pandas as pd
from retrying import retry
from shutil import copyfile
from stravalib.client import Client
from WarReportLogger import main_logger

def segment_details(num,segment,topguy,friend_df):
    id = num + 1
    segment_id = int(segment.id)
    segment_name = str(segment.name)
    segment_name = re.sub(',', "", segment_name)
    url = 'http://www.strava.com/segments/'+str(segment_id)+'/compare/'

    start_latitude = segment.start_latitude
    start_longitude = segment.start_longitude
    end_latitude = segment.end_latitude
    end_longitude = segment.end_longitude
    colour = friend_df.loc[friend_df['shortname'] == topguy,'colour'].values[0]
    topguy_fullname = friend_df.loc[friend_df['shortname'] == topguy,'name'].values[0]

    tuple=(str(num),str(start_latitude),str(start_longitude),str(segment_name)+':  ['+str(topguy_fullname)+']',str(topguy_fullname),str(colour),str(segment_name),str(segment_id),str(url))
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    print('\r'+str(now)+': ID: '+str(id)+'     Segment ID:  '+str(segment_id)+'   Owner:  '+str(topguy_fullname),)
    return tuple

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_leaderboard(client,j,club,timeframe=None):
    return client.get_segment_leaderboard(j,club_id=club,timeframe=timeframe)

def main(argv):
    if len(argv) == 1:
        print('read segoutput.csv')
        df1 = pd.read_csv('segoutput.csv',index_col=False)
        df1 = df1.set_index(['segment_id'])

    club = 202883
    client = Client(access_token='99c2994556a29905b96eb4197996854041ca47ca')

    timeframe=None
    segoutput = 'segoutput.csv'
    if len(argv) > 1:
        timeframe = argv[1]
        segoutput = 'segoutput_' + argv[1] + '.csv'
    segoutfile = open(segoutput, 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    segoutputlist = []

    friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)
    friend_count_dict = {}

    #Column #2 Segment_name
    s = pd.read_csv('segment_details.csv', index_col=2)
    for idx, segment in s.iterrows():
        num = int(segment.no)       
        j = int(segment.id)

        try:
            leaderboard = retry_get_leaderboard(client,j,club,timeframe)
            if not leaderboard:
                topguy = 'UNCLAIMED'
                topguy_id = 0
            else:
                topguy = leaderboard[0].athlete_name

            if not topguy in friend_df['shortname'].values:
                new_friend = {'name': topguy, 'id':'xxx', 'colour':'646464','shortname': topguy}
                friend_df = friend_df.append(new_friend, ignore_index=True)

            if topguy in friend_count_dict:
                friend_count_dict[topguy] += 1
            else:
                friend_count_dict[topguy] = 1

            for z in segment_details(num,segment,topguy,friend_df):
                segoutfile.write(str(z)+',')
            segoutfile.write('\n')

        except Exception as e:
            print(str(e))
            badoutfile = open('bad_segments.csv', 'a+')
            badoutfile.write(str(j)+','+'\n')
            badoutfile.close()
            pass

        time.sleep(1.5) #Strava limit 600/15mins

    segoutfile.close()
    
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    copyfile(segoutput, 'segment_history/' + segoutput.replace('.csv', '_' + now + '.csv'))
    
    friend_df.to_csv('friend_colour_new.csv', index=False)

    #segment count output
    segmentcount = 'segmentcount.csv'
    if len(argv) > 1:
        segmentcount = 'segmentcount_' + argv[1] + '.csv'
    segcountoutfile = open(segmentcount, 'w')
    segcountoutfile.write('name,colour,count'+'\n')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            print(str(x)+': '+str(friend_count_dict[x]))
            segcountoutfile.write(str(friend_df.loc[friend_df['shortname'] == x,'name'].values[0])+','+str(friend_df.loc[friend_df['shortname'] == x,'colour'].values[0])+','+str(friend_count_dict[x])+'\n')
    segcountoutfile.write('\n')
    segcountoutfile.close()

    #segment count over time output
    segmentcountovertime = 'segmentcountovertime.csv'
    if len(argv) > 1:
        segmentcountovertime = 'segmentcountovertime_' + argv[1] + '.csv'
    segcountovertimefile = open(segmentcountovertime, 'a+')
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            segcountovertimefile.write(str(nowdate)+','+str(friend_df.loc[friend_df['shortname'] == x,'name'].values[0])+','+str(friend_df.loc[friend_df['shortname'] == x,'colour'].values[0])+','+str(friend_count_dict[x])+'\n')
    segcountovertimefile.close()

    if len(argv) == 1:
        print("To mattermost")
        
        time.sleep(5)

        #read newly created segoutput.csv (df2) and compare it to original (df1):
        df2 = pd.read_csv('segoutput.csv',index_col=False)
        df2 = df2.set_index(['segment_id'])
        try:
            main_logger(df2,df1)
        except Exception as e:
            print('Error: '+str(e))
            pass

if __name__ == "__main__":
  main(sys.argv)
