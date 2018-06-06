git clone --mirror https://github.com/vigi4cure/vigi4cure.github.io
cd vigi4cure.github.io.git/
#copy bfg-1.13.0.jar .
java -jar bfg-1.13.0.jar --delete-files strava_segment_search.py
git reflog expire --expire=now --all && git gc --prune=now --aggressive
vi .git/confit
git push
