import re
import utils
import bs4
import urllib2


class WheelockSpider:

    base_url = 'http://www.wheelock.edu'
    courses = []
    course_set = set()

    def run(self):
        """
        Find all department links, spin off requests to parse each one
        """
        url = ('{}/academics/academic-records-and-registration/course-catalog'
               .format(self.base_url))
        web_page = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(web_page, 'lxml')
        section = soup.find('div', {'id': 'contentLeft'})
        department_links = section.find_all('ul')[5].find_all('a')
        for link in department_links:
            final = self.base_url + link.attrs['href']
            web_page = urllib2.urlopen(final).read()
            soup = bs4.BeautifulSoup(web_page, 'lxml')
            self.scrape_courses(soup)

    def scrape_courses(self, soup):
        """
        The site is laid out the following way:
        <p class="Heading-6-Courses"> -> has the course title and credits
        <p class="Course-Body"> -> description (sometimes more than one of
        these)
        """
        category = soup.select('#contentBody h1')[0].text.encode('ascii',
                                                                 'ignore')
        category = re.search(
            r'Course Catalog: (.*?) Courses', category
        ).groups(0)[0]
        div = soup.select('#contentLeft')[0]
        course = {}
        for child in div.children:
            if isinstance(child, bs4.element.NavigableString):
                continue
            if child.attrs == {'class': ['Heading-6-Courses']}:
                # New course.
                # We should close out the old course, and then parse the new
                # one.
                if course and course['title'] not in self.course_set:
                    course = utils.clean_course(course)
                    self.courses.append(course)
                    self.course_set.add(course['title'])

                # This element should look like this:
                # course abbreviation<br>title<br>credits
                contents = list(child.children)[0]
                contents = [a.string.encode('ascii', 'ignore')
                            for a in contents
                            if isinstance(a, bs4.element.NavigableString)]
                assert len(contents) == 3
                title = '{}: {}'.format(contents[0], contents[1])
                creds = re.sub(r' [cC]redit[s]{0,1}(.*?)$', '', contents[2])
                creds = re.sub(r'[ ]{0,1}-[ ]{0,1}', ' to ', creds)
                course = {
                    'category': category,
                    'title': title,
                    'credits': creds
                }
            elif ((child.attrs == {'class': ['Course-Body']} or
                    child.attrs == {'class': ['Body-Text']}) and
                    course):
                desc = child.text.encode('ascii', 'ignore')
                if 'description' in course:
                    course['description'] += ' ' + desc
                else:
                    course['description'] = desc


if __name__ == '__main__':
    spider = WheelockSpider()
    spider.run()
    utils.courses_to_csv(spider.courses, 'wheelock.csv')
