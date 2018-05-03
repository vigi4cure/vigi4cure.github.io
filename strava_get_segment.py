import time
from stravalib.client import Client
from retrying import retry

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_segment(client,j):
    return client.get_segment(j)

with open('/home/vgoobm/vigi4cure.github.io/segments.csv') as f:
    segment_IDs = f.readlines()

client = Client(access_token='99c2994556a29905b96eb4197996854041ca47ca')
f = open('/home/vgoobm/vigi4cure.github.io/segment_details.csv', 'w')
f.write('id,name,resource_state')
for s_id in segment_IDs:
    s = retry_get_segment(client,s_id)
    f.write(str(s.id) + ',"' + s.name + '",' + str(s.resource_state)) 
    time.sleep(1.5)
f.close()

    


