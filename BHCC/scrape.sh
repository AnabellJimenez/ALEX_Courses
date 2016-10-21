rm *.html*
wget -nd -r -np -k -A "*.html*" -I /subjects http://catalog.mit.edu/subjects
rm -f robots.txt
ls | grep html | python ./mit-scraper.py
rm *.html*
