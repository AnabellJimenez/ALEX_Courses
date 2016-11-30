import re
import urllib2
import utils
import bs4


class LasellSpider:

    courses = []
    department_map = {
        'AAC': 'Academic Achievement Center',
        'ANTH': 'Anthropology',
        'ARTH': 'Art History',
        'ARTS': 'Art Studio',
        'ASL': 'American Sign Language',
        'AT': 'Athletic Training',
        'BIO': 'Biology',
        'BUSS': 'Business',
        'CHEM': 'Chemistry',
        'COM': 'Communication',
        'CJ': 'Criminal Justice',
        'ECON': 'Economics',
        'ED': 'Education',
        'ENG': 'English',
        'ENV': 'Environmental Studies',
        'EXSC': 'Exercise Science',
        'FASD': 'Fashion Design And Production',
        'FASH': 'Fashion And Retail Merchandising, Communication, '
                'And Promotion',
        'FED': '',
        'FYA': '',
        'FYS': 'First Year Seminar',
        'FREN': 'French',
        'GLBS': 'Global Studies',
        'GRAP': 'Graphic Design',
        'HIST': 'History',
        'HON': 'Honors',
        'HEM': 'Hospitality Management',
        'HUM': 'Humanities',
        'HS': 'Human Services',
        'IDS': 'Interdisciplinary Studies',
        'IGS': 'Intergenerational Studies',
        'JPN': 'Japanese',
        'LS': 'Legal Studies',
        'MATH': 'Mathematics',
        'MAHT': 'Mathematics',
        'MDSC': 'Multidisciplinary Science',
        'MUS': 'Music',
        'PERF': 'Performing Arts',
        'PHIL': 'Philosophy',
        'PHYS': 'Physics',
        'POLS': 'Political Science',
        'PSYC': 'Psychology',
        'RAC': 'Research Across The Curriculum',
        'RSCI': 'Rehabilitation Science',
        'SCI': 'Science',
        'SVL': 'Service Learning',
        'SJA': 'Social Justice Activism',
        'SOC': 'Sociology',
        'SPAN': 'Spanish',
        'SPED': 'Special Education',
        'SS': 'Social Studies',
        'SMGT': 'Sport Management'

    }

    def run(self):
        """
        There's only one page for Lasell College with all the info on it,
        so this function does all that.
        """
        url = ('http://www.lasell.edu/academics/academic-catalog'
               '/undergraduate-catalog/course-descriptions.html')

        web_page = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(web_page, 'lxml')

        # ALl the courses are in the #tab-3 element. The element is
        # structured very neatly:
        # <h4> --> title
        # <p>  --> description
        courses_titles = soup.select('#tab-3 h4')
        for title in courses_titles:
            course = {}
            course['title'] = title.text.strip()
            # Find the department.
            department = re.search(r'([A-Z]{2,4})[0-9]', course['title'])
            if department:
                abbrev = department.groups(0)[0]
                course['department'] = self.department_map.get(abbrev)
            else:
                course['department'] = None

            desc = title.find_next_sibling()
            if desc:
                course['description'] = desc.text.strip()
            else:
                course['description'] = None
            self.courses.append(utils.clean_course(course))

if __name__ == '__main__':
    spider = LasellSpider()
    spider.run()
    utils.courses_to_csv(spider.courses, 'lasell_college.csv')
