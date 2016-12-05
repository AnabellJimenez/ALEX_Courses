cd ./berklee
ls |grep -v '\.py' |xargs rm
wget -nd -r -np -k -I /online-registration-manual/course-descriptions/ https://www.berklee.edu/online-registration-manual/course-descriptions/arranging
rm -f robots.txt # This is unnecesary
ls | python ./berklee-scraper.py
ls |grep -v .py| xargs rm
