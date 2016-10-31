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
        return "Not Offered"
    return terms[:-2]


def courseExtract(course):
    courseDic = {}
    courseInfo = BeautifulSoup(course, "lxml")
    courseName = courseInfo.find(class_="courseblocktitle").text
    # preReq = courseInfo.find(class_="courseblockprereq").text
    descr = courseInfo.find(class_="courseblockdesc").text
    credits = courseInfo.find(class_="courseblockhours").text
    rawTerms = courseInfo.find(class_="courseblockterms").text

    courseId = courseName[:courseName.index(" ")]
    courseTitle = courseName[courseName.index(" "):]
    courseNumber = courseId.split(".")[0]

    try:
        # This will fail if professor is not specified e.g. research subjects
        profs = courseInfo.find(class_="courseblockinstructors").text
    except:
        profs = "None"
    try:
        # Sometimes classes are not credit defined this only fails when not defined
        creditsSum = int(credits.split("-")[0])+int(credits.split("-")[1])+int(credits.split("-")[2].split(" ")[0])
    except:
        creditsSum = "Not Defined"

    courseDic["Course Id"] = courseId.encode('ascii', 'ignore')
    courseDic["Course Title"] = courseTitle.encode('ascii', 'ignore')
    courseDic["Course Number"] = courseNumber.encode('ascii', 'ignore')
    courseDic["Course Description"] = descr.encode('ascii', 'ignore')
    courseDic["Professors"] = profs.encode('ascii', 'ignore')
    courseDic["Term"] = getTerms(rawTerms)
    courseDic["Credits"] = creditsSum
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

            for course in soup.findAll("div", class_="courseblock"):
                courses.append(courseExtract(course.__str__()))
    except EOFError:
        # Reached the end of the input
        pass
    outputToCsv("../CSV-info/mit.csv", courses)
