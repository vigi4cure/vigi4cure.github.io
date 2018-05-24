#!/usr/bin/python3

import time
import numpy as np
from stravalib.client import Client

client = Client(access_token='99c2994556a29905b96eb4197996854041ca47ca')

# bounds = (45.380184 , -74.023017, 45.719182 ,  -73.436622)
flist = open('slist.txt', 'w')
ferror = open('serror.txt', 'w')
# for x in np.arange(45.28,45.71,0.05):
    # for y in np.arange(-74.12, -73.43, 0.07):
        # bounds = (x, y, x+0.075, y+0.105)
for x in np.arange(45.380184,45.719182-0.03,0.03):
    for y in np.arange(-74.023017, -73.436622-0.05, 0.05):
        bounds = (x, y, x+0.045, y+0.075)
        # activityType = activityType_example # String | Desired activity type. (optional)
        # minCat = 56 # Integer | The minimum climbing category. (optional)
        # maxCat = 56 # Integer | The maximum climbing category. (optional)
        try:
            segments = client.explore_segments(bounds)
            print(len(segments))
            for segment in segments:
                flist.write(str(segment.id) + '\n')
        except:
            print('%.6f,%.6f,%.6f,%.6f\n' % (x, y, x+0.045, y+0.075))
            ferror.write('%.6f,%.6f,%.6f,%.6f\n' % (x, y, x+0.045, y+0.075))
            # pass
        time.sleep(1.5)
flist.close()
ferror.close()
