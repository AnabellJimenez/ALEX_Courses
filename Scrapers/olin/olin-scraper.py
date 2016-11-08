import csv
from bs4 import BeautifulSoup

def getTerms(rawTerms):
    terms = ""
    if "spring" in rawTerms.lower():
        terms += "Spring, "
    if "fall" in rawTerms.lower():
        terms += "Fall, "
    if "summer" in rawTerms.lower():
        terms += "IAP, "
    if "summer" in rawTerms.lower():
        terms += "Summer, "
    if terms =="":
        return "Not Offered, "
    return terms[:-2]


def courseExtract(course):
    courseDic = {}
    courseInfo = BeautifulSoup(course, "lxml")
    courseName = courseInfo.find(class_="course-title").text.encode('ascii', 'ignore')
    courseCredit = courseInfo.find(class_="field-course-credits").text.encode('ascii', 'ignore').replace("\t", "")
    courseDescr = courseInfo.findAll("p")[-1].text.encode('ascii', 'ignore').replace("\t", "")


    courseArea = courseName[:4]
    courseNum = courseName[4:8]
    courseTitle = courseName.split("-")[1]
    courseDic["Course Area"] = courseArea
    courseDic["Course Num"] = courseNum
    courseDic["Course Title"] = courseTitle
    courseDic["Course Description"] = courseDescr
    courseDic["Credit"] = courseCredit
    return courseDic


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
        courses = []
        while True:
            file_name = raw_input()
            print file_name
            soup = BeautifulSoup(open(file_name), "lxml")

            for course in soup.findAll("article", class_="course-listing"):
                courses.append(courseExtract(course.__str__()))
    except EOFError:
        # Reached the end of the input
        pass
    outputToCsv("../../CSV-info/olin.csv", courses)
