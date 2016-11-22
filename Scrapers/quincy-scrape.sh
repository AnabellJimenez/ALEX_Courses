cd ./quincy
wget -nd -r "https://register.quincycollege.edu/m/d/m/c527f9fa-1165-452d-88e5-0577ac1122ba/CourseSearch/SearchResults?termcode=2016;10&title=&code=&department=&faculty=&campus=&additional=&openseats=OpenFull&add=T"

ls | grep -v CourseKey | grep -v py | xargs rm
ls |grep -v .py| xargs rm
