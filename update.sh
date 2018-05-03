#!/bin/bash

/usr/bin/git pull
/usr/bin/python3 segment_plots.py
/usr/bin/python3 strava_leaderboard.py
/usr/bin/python3 strava_segments.py
/usr/bin/git add -A
/usr/bin/git commit -a -m "$(date)"
/usr/bin/git push

