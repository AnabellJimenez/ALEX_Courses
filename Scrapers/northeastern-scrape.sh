cd ./northeastern
rm *.html*
wget -nd -r -np -k -A "*.html*" -I /course-descriptions http://catalog.northeastern.edu/course-descriptions/ 
rm -f robots.txt
ls | grep html | python ./northeastern-scraper.py
rm *.html*
