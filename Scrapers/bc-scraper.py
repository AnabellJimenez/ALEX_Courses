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

            try:
                courseTitleString = soup.find("h2", class_="course-title").text.encode('ascii', 'ignore')
                courseDescription = soup.find("p", class_="course-description").text.encode('ascii', 'ignore')
            except:
                continue

            courseArea = courseTitleString.split(" ")[0]
            courseNum = courseTitleString.split(" ")[1]
            courseTitle = ' '.join(courseTitleString.split("(")[0].split(" ")[2:])
            print courseTitleString
            s = ' '.join(courseTitleString.split("(")[-1].split(","))
            courseCredit = [int(s) for s in s.split() if s.isdigit()][0]
            
            courseNums.append(courseNum)
            courseTitles.append(courseTitle)
            courseCredits.append(courseCredit)
            courseAreas.append(courseArea)
            courseDescriptions.append(courseDescription)
            print courseArea, courseNum, courseTitle, courseCredit
            


    except EOFError:
        # Reached the end of the input
        pass

    # Zip courses
    courses = []
    for i in xrange(len(courseNums)):
        course = {}
        course["Title"] = courseTitles[i]
        course["Credits"] = courseCredits[i]
        course["Description"] = courseDescriptions[i]
        course["Id"] = courseNums[i]
        course["Category"] = courseAreas[i]
        courses.append(course)

    outputToCsv("../../CSV-info/bc.csv", courses)
