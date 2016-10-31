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
            soup = BeautifulSoup(open(file_name), "lxml")

            courseArea = soup.find("h1")
            numClasses = len(soup.findAll("div", class_="courseNum"))

            # This iterates addding one courseArea for each class so the arrays
            # stay the same lenght making it easier to make a dictionary of it
            # later.

            for i in xrange(numClasses):
                courseAreas.append(courseArea)

            courseNums.extend(soup.findAll("div", class_="courseNum"))
            courseTitles.extend(soup.findAll("div", class_="courseTitle"))
            courseCredits.extend(soup.findAll("div", class_="courseCredits"))
            courseDescriptions.extend(soup.findAll("div", class_="courseDescription"))

    except EOFError:
        # Reached the end of the input
        pass

    # Zip courses
    courses = []
    for i in xrange(len(courseNums)):
        course = {}
        course["Title"] = courseTitles[i].text.encode('ascii', 'ignore')
        course["Credits"] = courseCredits[i].text.encode('ascii', 'ignore')
        course["Description"] = courseDescriptions[i].text.encode('ascii', 'ignore')
        course["Id"] = courseNums[i].text.encode('ascii', 'ignore')
        course["Category"] = courseAreas[i].text.encode('ascii', 'ignore')
        courses.append(course)

    outputToCsv("../../CSV-info/bhcc.csv", courses)
