import csv
from bs4 import BeautifulSoup


def outputToCsv(filename, courses):
    keys = courses[0].keys()

    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(courses)

if __name__ == "__main__":
    try:
        courseNums = []
        courseTitles = []
        courseCredits = []
        courseDescriptions = []
        courseAreas = []
        courseSections = []
        courseOpenings = []
        courseTimes = []
        courseDates = []
        while True:
            file_name = raw_input()
            if(".py" in file_name):
                continue
            
            print file_name
            soup = BeautifulSoup(open(file_name), "lxml")

            courseNum = soup.find(class_="subtext").text.encode('ascii','ignore')

            courseAreas.append(courseNum.split(" ")[0])
            courseNums.append(courseNum.split(" ")[1])
            courseSections.append(' '.join(courseNum.split(" ")[2:]))

            courseOpening = soup.find(class_="green")

            # This is in the case there are few left
            if courseOpening is None:
                courseOpening = soup.find(class_="yellow")

            # This is in the case no openings left in the course
            if courseOpening is None:
                courseOpening = soup.find(class_="red")

            courseOpenings.append(courseOpening.text.encode('ascii', 'ignore'))

            courseTitle = soup.find(class_="boldText").text.encode('ascii', 'ignore')
            courseTitles.append(courseTitle)

            courseInfos = soup.findAll(class_="header")

            courseTime = ''
            courseDate = ""
            for courseInfo in courseInfos:
                if courseInfo.text == "Schedule":
                    courseTime = courseInfo.next_sibling.next_sibling.text.encode("ascii",
                    "ignore")
                    courseDate = courseInfo.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.encode('ascii', 'ignore')

                if courseInfo.text == "Details":
                    courseCredit = courseInfo.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling

                if courseInfo.text == "Description":
                    courseDescription = courseInfo.next_sibling.next_sibling

            courseCredits.append(courseCredit.text.encode('ascii', 'ignore'))
            courseTimes.append(courseTime)
            courseDates.append(courseDate)
            courseDescriptions.append(courseDescription.text.encode('ascii', 'ignore'))


    except EOFError:
        # Reached the end of the input
        pass

    # Zip courses
    courses = []
    print len(courseDescriptions), len(courseTitles)
    for i in xrange(len(courseNums)):
        course = {}
        course["Title"] = courseTitles[i]
        course["Description"] = courseDescriptions[i]
        course["Id"] = courseNums[i]
        course["Category"] = courseAreas[i]
        course["Section"] = courseSections[i]
        course["Openings"] = courseOpenings[i]
        courses.append(course)

    outputToCsv("../../CSV-info/quincy.csv", courses)
