#!/bin/bash

#cd ~/vigi4cure.github.io
echo cd /home/vgoobm/Tools/Misc/vigi4cure.github.io
cd /home/vgoobm/Tools/Misc/vigi4cure.github.io

# echo /usr/bin/git pull
# /usr/bin/git pull
echo /usr/bin/python3 strava_leaderboard.py
/usr/bin/python3 strava_leaderboard.py
echo /usr/bin/python3 segment_plots.py
/usr/bin/python3 segment_plots.py
echo /usr/bin/python3 strava_segments.py
/usr/bin/python3 strava_segments.py
echo /usr/bin/git add -A
/usr/bin/git add -A
echo /usr/bin/git commit -a -m "$(date)"
/usr/bin/git commit -a -m "$(date)"
echo /usr/bin/git push
/usr/bin/git push

