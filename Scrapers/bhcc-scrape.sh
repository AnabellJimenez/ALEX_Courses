rm *index*
wget -nd -r -np -k -I /catalog/courses http://www.bhcc.mass.edu/catalog/courses/index.php
rm -f index.php # this file has no information and errors out because of that 
rm -f robots.txt # This is unnecesary
echo $pwd
ls | grep php | python ./bhcc-scraper.py
rm *index*
