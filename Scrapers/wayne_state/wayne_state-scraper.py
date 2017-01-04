import csv
from bs4 import BeautifulSoup


def outputToCsv(filename, courses):
    keys = courses[0].keys()
    for dic in courses:
        if dic.keys() != keys:
            print dic.keys(), keys

    print "Outputting to file", filename
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(courses)

if __name__ == "__main__":
    try:
        print "start"
        courseDescriptions = []
        courseNums = []
        courseTitles = []
        courseCredits = []
        courseAreas = []

        while True:
            file_name = raw_input()
            print file_name
            soup = BeautifulSoup(open(file_name), "lxml")
            if '.py' in file_name:
                continue
            courseArea = soup.find("p", class_="FM_Hd22").text.encode('ascii', 'ignore')
            print courseArea

            for course in soup.findAll("p", class_="FM_ct"):
                courseDescription = course.text.encode('ascii', 'ignore')
                if courseDescription == '':
                    continue
                courseDescriptions.append(courseDescription)

            for course in soup.findAll("p", class_="FM_chs"):
                titleString = course.text.encode('ascii', 'ignore')
                if titleString == '':
                    continue

                courseNums.append(titleString.split(" ")[0])
                courseTitles.append(' '.join(titleString.split(" ")[1:]).split(".")[0])
                courseCredits.append(''.join(titleString.split(".")[2:]))
                courseAreas.append(courseArea)


            print len(courseTitles), len(courseDescriptions)
            if len(courseTitles) != len(courseDescriptions):
                raise Exception("Offset Error")

    except EOFError:
        # Reached the end of the input
        pass
    courses = []
    for i in xrange(len(courseNums)):
        course = {}
        course["Title"] = courseTitles[i]
        course["Credits"] = courseCredits[i]
        course["Description"] = courseDescriptions[i]
        course["Id"] = courseNums[i]
        course["Category"] = courseAreas[i]
        courses.append(course)
    outputToCsv("../../CSV-info/wayne_state.csv", courses)
