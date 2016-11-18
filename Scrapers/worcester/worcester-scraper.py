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
        while True:
            file_name = raw_input()
            print file_name
            soup = BeautifulSoup(open(file_name), "lxml")

            courseTitlesContainer = soup.findAll("h3")
            courseDescrs = soup.findAll("p")

            # This iterates addding one courseArea for each class so the arrays
            # stay the same lenght making it easier to make a dictionary of it
            # later.
            for courseTitleContainer in courseTitlesContainer:
                courseTitle = courseTitleContainer.text.encode('ascii', 'ignore')
                courseAreas.append(courseTitle.split(" ")[0])
                courseNums.append(courseTitle.split(" ")[1][:-1])
                courseTitles.append(' '.join(courseTitle.split(" ")[2:]))
                courseDescr = courseTitleContainer.findNext("p")
                courseDescrText = courseDescr.text.encode('ascii', 'ignore')
                courseDescriptions.append(courseDescrText.replace("\n", " "))

            print len(courseDescriptions), len(courseTitles)
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
        courses.append(course)

    outputToCsv("../../CSV-info/worcester.csv", courses)
