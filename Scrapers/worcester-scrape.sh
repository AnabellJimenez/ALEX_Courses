cd ./worcester
wget https://web.wpi.edu/academics/catalogs/ugrad/aecourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/ascourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/arencourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/basic-sciencecourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/bbcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/becourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/mgcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/cmcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/chcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/cecourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/cscourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/eecourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/escourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/fpcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/hucourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/imgdcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/idcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/macourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/mecourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/mscourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/phcourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/rbecourses.html
wget https://web.wpi.edu/academics/catalogs/ugrad/sscourses.html
ls |grep html | python ./worcester-scraper.py
rm *.html
