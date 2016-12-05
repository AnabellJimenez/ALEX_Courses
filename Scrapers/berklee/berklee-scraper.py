import csv
from bs4 import BeautifulSoup


def courseExtract(course):

    courseDic = {}
    courseInfo = BeautifulSoup(course, "lxml")
    try:
        # This happens when they put registrar name in one of these don't care
        # about data there.
        courseTitle = courseInfo.find("h2").text
    except:
        return

    courseNum = courseInfo.find("h3", class_="course-number").text
    try:
        courseDescr = courseInfo.find("p").text
        courseDic["Course Description"] = courseDescr.encode('ascii', 'ignore')
    except:
        courseDic["Course Description"] = ''
    courseData= courseInfo.findAll("span")
    courseInfos = ""
    creditsSum = courseInfo.find("em").text.encode('ascii', 'ignore')

    for courseDatum in courseData:
        try:
            courseInfos += courseDatum.text.encode("ascii", "ignore")
            courseInfos += str(courseDatum.next_sibling.encode("ascii", "ignore"))
            courseInfos += '\n'
        except:
            pass
            



    courseDic["Course Title"] = courseTitle.encode('ascii', 'ignore')
    courseDic["Course Number"] = courseNum.encode('ascii', 'ignore')
    courseDic["Info"] = courseInfos.encode('ascii', 'ignore')
    courseDic["Credits"] = creditsSum
    return courseDic


def outputToCsv(filename, courses):
    keys = courses[0].keys()

    print "Outputting to file", filename
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(courses)

if __name__ == "__main__":
    try:
        courses = []
        while True:
            file_name = raw_input()
            print file_name
            soup = BeautifulSoup(open(file_name), "lxml")

            for course in soup.findAll("div", class_="views-row-even"):
                course = courseExtract(course.__str__())
                if course == None:
                    continue
                courses.append(course)

            for course in soup.findAll("div", class_="views-row-odd"):
                course = courseExtract(course.__str__())
                if course == None:
                    continue
                courses.append(course)

    except EOFError:
        # Reached the end of the input
        pass
    outputToCsv("../../CSV-info/berklee.csv", courses)
