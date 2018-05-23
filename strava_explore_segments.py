#!/usr/bin/python3

import time
import numpy as np
from stravalib.client import Client

client = Client(access_token='99c2994556a29905b96eb4197996854041ca47ca')

# bounds = (45.380184 , -74.023017, 45.719182 ,  -73.436622)
f = open('slist.txt', 'w')
bounds = (45.380184 , -74.023017, 45.430184 , -73.973017)
for x in np.arange(45.35,45.71,0.05):
    for y in np.arange(-74.07, -73.43, 0.07):
        bounds = (x, y, x+0.07, y+0.09)
        # activityType = activityType_example # String | Desired activity type. (optional)
        # minCat = 56 # Integer | The minimum climbing category. (optional)
        # maxCat = 56 # Integer | The maximum climbing category. (optional)
        segments = client.explore_segments(bounds)
        print(len(segments))
        for segment in segments:
            f.write(str(segment.id) + '\n')
        time.sleep(2)
f.close()
