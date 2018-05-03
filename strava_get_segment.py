import time
from stravalib.client import Client
from retrying import retry

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_segment(client,j):
    return client.get_segment(j)

with open('segments.csv') as f:
    segment_IDs = f.readlines()

client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
f = open('segment_details.csv', 'w')
for s_id in segment_IDs:
    s = retry_get_segment(client,s_id)
    f.write(str(s.id) + ',"' + s.name + '",' + str(s.resource_state)) 
    time.sleep(1.5)
f.close()

    


