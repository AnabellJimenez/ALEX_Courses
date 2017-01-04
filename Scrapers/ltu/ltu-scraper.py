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

            for course in soup.findAll("td", class_="nttitle"):
                courseTitleInfo = course.text.encode('ascii', 'ignore')
                courseAreas.append(courseTitleInfo.split(" ")[0])
                courseNums.append(courseTitleInfo.split(" ")[1])
                courseTitles.append(' '.join(courseTitleInfo.split(" ")[3:]))
                courseDescrInfo = course.parent.next_sibling.next_sibling.text.encode('ascii', 'ignore').strip(' \t\n\r')
                courseDescriptions.append(courseDescrInfo)
                for courseInfo in courseDescrInfo.split("\n"):
                    if "Credit" in courseInfo:
                        courseCredits.append(courseInfo.split(".")[0])
                        break


            print len(courseTitles), len(courseCredits)

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
    outputToCsv("../../CSV-info/ltu.csv", courses)
