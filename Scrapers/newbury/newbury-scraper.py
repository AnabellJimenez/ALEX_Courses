import re
import csv
from bs4 import BeautifulSoup, NavigableString, Tag

classRegex = re.compile("^[A-Z][A-Z][0-9]+")

def containsClasses(classesTree):
    firstClass = classesTree.find("a")

    if firstClass == None:
        return False

    return classRegex.match(firstClass.get("name","")) != None


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
            htmlTree = BeautifulSoup(open(file_name), "lxml")
            generalDiv = htmlTree.find("div", class_="col-md-12 pt-xl")
            classesTree = BeautifulSoup(str(generalDiv), "lxml")

            if containsClasses(classesTree):
                on = False

                for child in generalDiv.childGenerator():
                    if isinstance(child, NavigableString):
                        if "." in str(child.encode("ascii", "ignore")):
                            courseDescriptions.append(child.split("\n")[1])

                classes = classesTree.findAll("h2")
                for singleClass in classes:
                    classInfo = []
                    singleClassText = singleClass.text.encode('ascii', 'ignore')
                    # The strip is to remove and random newlines at the beginning
                    classId = singleClassText.split(" ")[0].strip("\n")
                    try:
                        # this splits and finds the last parenthiss then the first word
                        # in the parenthesis. Works on all the html
                        classCredits = int(singleClassText.split("(")[-1].split(" ")[0])

                        '''
                        This stuff removes the credit off the end of string to get class
                        name. Rfind finds the last element of the index int the string'''

                        creditIndex = singleClassText.rfind(str(classCredits))
                        courseName = singleClassText[len(classId)+1:creditIndex-1]

                    except:

                        ''' This only gets hit if there is no class credit, and only one
                        course doesn't have a class credit. Just assumes no credit'''
                        classCredits = "Undefined"
                        courseName = singleClassText[len(classId)+1:]

                    courseNums.append(classId)
                    courseTitles.append(courseName)
                    courseCredits.append(classCredits)
                    courseAreas.append(classId[:2])
    except EOFError:
        # Reached the end of the input
        pass

    courses = []
    for i in xrange(len(courseNums)):
        course = {}
        course["Title"] = courseTitles[i].encode('ascii', 'ignore')
        course["Credits"] = courseCredits[i]
        course["Description"] = courseDescriptions[i].encode('ascii', 'ignore')
        course["Id"] = courseNums[i].encode('ascii', 'ignore')
        course["Category"] = courseAreas[i].encode('ascii', 'ignore')
        courses.append(course)

    outputToCsv("../../CSV-info/newburry.csv", courses)
