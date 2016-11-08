cd ./olin
rm *html*
wget -nd -r -np -I /course-listing/ http://www.olin.edu/course-listing
rm robots.txt
rm *\?*
ls|python olin-scraper.py
rm *html*
