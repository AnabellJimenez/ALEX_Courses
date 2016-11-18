# coding: utf-8
f = open('mcla.txt', 'r')
data = f.read()
courses2 = data.split('\n\n')

courses3 = []
for course in courses2:
    courses3.append(course.split('\n'))

category_key = {
    "AMGT": "ARTS MANAGEMENT",
    "ANTH": "ANTHROPOLOGY",
    "ART": "ART",
    "ATTR": "ATHLETIC TRAINING",
    "BADM": "BUSINESS ADMINISTRATION",
    "BIOL": "BIOLOGY",
    "CCAP": "CORE CAPSTONE",
    "CCCA": "CORE CREATIVE ARTS",
    "CCHH": "CORE HUMAN HERITAGE",
    "CCSS": "CORE SELF AND SOCIETY",
    "CCST": "CORE SCIENCE AND TECHNOLOGY",
    "CHEM": "CHEMISTRY",
    "CSCI": "COMPUTER SCIENCE AND INFORMATION SYSTEMS",
    "ECON": "ECONOMICS",
    "EDUC": "EDUCATION",
    "ENGL": "ENGLISH/COMMUNICATIONS",
    "ENVI": "ENVIRONMENTAL STUDIES",
    "ERTH": "EARTH SCIENCE",
    "FPA": "FINE AND PERFORMING ARTS",
    "FREN": "FRENCH",
    "HIST": "HISTORY",
    "HONR": "HONORS",
    "IDST": "INTERDISCIPLINARY STUDIES",
    "ITAL": "ITALIAN",
    "MATH": "MATHEMATICS",
    "MODL": "MODERN LANGUAGE",
    "MUSI": "MUSIC",
    "PHED": "PHYSICAL EDUCATION",
    "PHIL": "PHILOSOPHY",
    "PHYS": "PHYSICS",
    "POSC": "POLITICAL SCIENCE",
    "PSYC": "PSYCHOLOGY",
    "SKIL": "SKILL",
    "SOCI": "SOCIOLOGY",
    "SOWK": "SOCIAL WORK",
    "SPAN": "SPANISH",
    "THEA": "THEATER",
    "TRVL": "TRAVEL",
    "WMST": "WOMEN'S STUDIES",
}

courses4 = []
for course in courses3:
    if len(course) > 1:
        desc = ' '.join(course[2:-1])
        cat = category_key.get(course[0].split(' ')[0], None)
        if not cat:
            print 'skipping', course
            continue
        new = {
            'title': course[0],
            'credits': course[1],
            'description': desc,
            'prerequisites': course[-1],
            'category': cat
        }
        courses4.append(new)
    else:
        print 'skipping', course


f = open('../../CSV-info/mcla.csv', 'w')
import csv
w = csv.writer(f)
w.writerow(['category', 'title', 'credits', 'prerequisites', 'description'])
for course in courses4:
    try:
        w.writerow([
            course['category'],
            course['title'],
            course['credits'],
            course['prerequisites'],
            course['description']
        ])
    except:
        print 'shit'

