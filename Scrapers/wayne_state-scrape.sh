cd ./wayne\_state
rm *\'*
ls | grep -v '\.py' | xargs rm 
wget -nd np -k -I /ubk\-output -r http://www.bulletins.wayne.edu/ubk-output/index.html
rm ./General_Education_Courses.htm
rm *\'*
ls | grep -v Course | grep -v '\.py' | xargs rm

ls | python ./wayne\_state-scraper.py
ls | grep -v '\.py' | xargs rm 
