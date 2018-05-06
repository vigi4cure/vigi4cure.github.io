#!/usr/bin/python3

import csv, time
from stravalib.client import Client
from retrying import retry

def retry_get_segment(client,j):
    return client.get_segment(j)

def main():
    #reload(sys)
    #sys.setdefaultencoding('utf8')

    # df1 = pd.read_csv('segoutput.csv',index_col=False)
    # df1 = df1.set_index(['segment_id'])

    segmentlist = []
    file = open('segments_all.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])


    # club = 202883
    client = Client(access_token='99c2994556a29905b96eb4197996854041ca47ca')

    # segoutfile = open('segoutput.csv', 'w')
    # segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    # segoutputlist = []


    # friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)

    # friend_count_dict = {}

    segoutfile = open('segments_details.csv', 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    
    box = [[45.719182 , -74.023017], [45.380184 ,  -73.436622]]
    for num,j in enumerate(segmentlist):
        print(num)
        segment = retry_get_segment(client,j)
        print(segment.start_latitude)
        # try:
            # leaderboard = retry_get_leaderboard(client,j,club)
            # if not leaderboard:
                # topguy = 'UNCLAIMED'
                # topguy_id = 0

            # else:
                # topguy = leaderboard[0].athlete_name

                # topguy_id = leaderboard[0].athlete_id


            # if not topguy in friend_df['shortname'].values:
                # new_friend = {'name': topguy, 'id':'xxx', 'colour':'646464','shortname': topguy}
                # friend_df = friend_df.append(new_friend, ignore_index=True)


            # if topguy in friend_count_dict:
                # friend_count_dict[topguy] += 1
            # else:
                # friend_count_dict[topguy] = 1



            # for z in segment_details(num,segment,topguy,friend_df):
                # segoutfile.write(str(z)+',')
            # segoutfile.write('\n')


        # except Exception:
            # badoutfile = open('bad_segments.csv', 'a+')
            # badoutfile.write(str(j)+','+'\n')
            # badoutfile.close()
            # pass
        time.sleep(1.5)



    # segoutfile.close()
    # friend_df.to_csv('friend_colour_new.csv', index=False)


    #segment count output
    # segcountoutfile = open('segmentcount.csv', 'w')
    # segcountoutfile.write('name,colour,count'+'\n')
    # for x in friend_count_dict:
        # if x != 'UNCLAIMED':
            # print(str(x)+': '+str(friend_count_dict[x]))
            # segcountoutfile.write(str(friend_df.loc[friend_df['shortname'] == x,'name'].values[0])+','+str(friend_df.loc[friend_df['shortname'] == x,'colour'].values[0])+','+str(friend_count_dict[x])+'\n')
    # segcountoutfile.write('\n')
    # segcountoutfile.close()


    # segment count over time output
    # segcountovertimefile = open('segmentcountovertime.csv', 'a+')
    # nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
    # for x in friend_count_dict:
        # if x != 'UNCLAIMED':
            # segcountovertimefile.write(str(nowdate)+','+str(friend_df.loc[friend_df['shortname'] == x,'name'].values[0])+','+str(friend_df.loc[friend_df['shortname'] == x,'colour'].values[0])+','+str(friend_count_dict[x])+'\n')
    # segcountovertimefile.close()

    # time.sleep(5)

    # read newly created segoutput.csv (df2) and compare it to original (df1):
    # df2 = pd.read_csv('segoutput.csv',index_col=False)
    # df2 = df2.set_index(['segment_id'])
    # try:
        # main_logger(df2,df1)
    # except Exception as e:
        # print('Error: '+str(e))
        # pass



if __name__ == "__main__":
  main()

