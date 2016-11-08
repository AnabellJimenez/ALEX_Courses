cd ./newbury
rm -vf *html*
rm -rf ./www.newbury*
wget -I /academics -r -k https://www.newbury.edu/academics/academic-resources/academic-catalog.html
find . | grep -v course-descriptions | rm -f # This removes anything that is not a course description
find . |grep html |  xargs -I '{}' mv {} ./ # This moves all the html files into  a single directory so its easier to scan
rm -rf ./www.newbury*
ls | grep html | python newbury-scraper.py
rm -f *.html
