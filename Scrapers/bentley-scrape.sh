cd ./bentley
rm *undergraduate*
wget -l 1 -nd -r http://www.bentley.edu/offices/registrar/undergraduate-courses
mv ./gb ../
ls | grep -v undergraduate | grep -v py | xargs rm
mv ../gb ./ # They didn't name theirs as undergrad course. Its the only one so this is a decent work around
ls | python bentley-scraper.py
ls | grep -v bentley-scraper.py | xargs rm
