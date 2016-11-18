import bs4
import re

import utils
from utils import courses_to_csv


def scrape():
    html = open('necc_spring_2017.html', 'r')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    url = 'https://ssb.necc.mass.edu:9030'

    rows = soup.select('table.datadisplaytable tr')

    # Every odd row is the title of the course
    # Every even row is the info about the course
    # So we need to parse them as couples

    courses = []

    for i in range(0, len(rows) - 1, 2):
        course = {}
        # TITLE
        course['title'] = rows[i].text.strip().encode('ascii', 'ignore')
        course['link'] = url + rows[i].find('a').attrs['href']

        # DESCRIPTION
        # text in wrapper <td> element, before <br>
        td = rows[i + 1].find('td')
        desc = td.next_element
        course['description'] = desc.strip()
        if desc.next_element.name == 'b':
            # PREREQUISITES
            # looks like "Prerequisite(s): bunch of stuff
            # just want stuff after the first colon
            # also in some cases, there is a newline with non-prereq info.
            # cut that out as well.
            all_prereq_text = desc.next_element.text.strip()
            just_prereqs = ''.join(
                all_prereq_text.split(': ')[1:]
            ).split('\n')[0]
            course['prerequisites'] = just_prereqs
        else:
            course['prerequisites'] = None

        # CREDITS
        # ???

        # LEVELS
        spans = td.select('.fieldlabeltext')
        try:
            course['levels'] = spans[0].next_sibling.strip()
        except IndexError:
            course['levels'] = None

        # SCHEDULE TYPE
        # first text after the second span
        # sometimes they are wrapped in <a>, sometimes not
        try:
            if spans[1].next_sibling.name == 'a':
                items = spans[1].find_next_siblings('a')
                course['schedule_type'] = ', '.join([s.string.strip()
                                                     for s in items])
            else:
                course['schedule_type'] = spans[1].next_sibling.string.strip()
        except IndexError:
            course['schedule_type'] = None

        # DEPARTMENT
        # usually after a newline, always has word Department
        # extract just the important bit
        department_matches = re.search('\\n[ a-zA-Z&]{1,}Department', td.text)
        if department_matches:
            department = re.sub('\\n[ ]{1,}', '', department_matches.group(0))
            course['department'] = department.replace(' Department', '')
        else:
            course['department'] = None

        print course['title']
        courses.append(utils.clean_course(course))

    return courses


if __name__ == '__main__':
    courses = scrape()
    courses_to_csv(courses, 'necc.csv')
