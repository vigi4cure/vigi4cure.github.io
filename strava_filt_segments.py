#!/usr/bin/python3

import csv, time
from stravalib.client import Client
from retrying import retry

def retry_get_segment(client,j):
    return client.get_segment(j)

def main():
    segmentlist = []
    file = open('segments_all.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])

    client = Client(access_token='99c2994556a29905b96eb4197996854041ca47ca')
    segoutfile = open('segment_details.csv', 'w')
    segoutfile.write('id,segment_id,segment_name,resource_state,start_latitude,start_longitude,end_latitude,end_longitude'+'\n')

    segbad = open('segment_bad.csv', 'w')
    segbad.write('Segment ID\n')

    box = [[45.719182 , -74.023017], [45.380184 ,  -73.436622]]
    for num,j in enumerate(segmentlist):
        try:
            seg = retry_get_segment(client,j)
            print(str(j))
            segoutfile.write('%s,%s,"%s",%s,%s,%s,%s,%s\next'%(num,
                                                               seg.id,
                                                               seg.name,
                                                               seg.resource_state,
                                                               seg.start_latitude,
                                                               seg.start_longitude,
                                                               seg.end_latitude,
                                                               seg.end_longitude))
            # segoutfile.write(str(num) + ',' )
            # print(type(segment))
        except Exception as e:
            print(str(j) + ':' + str(e))
            segbad.write(str(j) + '\n')
        time.sleep(1.5)

    segoutfile.close()
    segbad.close()

if __name__ == "__main__":
  main()

