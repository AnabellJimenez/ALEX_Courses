import urllib2
import utils
import bs4
import re
from string import ascii_lowercase


class SimmonsSpider:

    url = 'http://courses.simmons.edu/spring/'
    courses = []

    def run(self):
        """
        Download each of the web pages in the course index, e.g. /a, /b, /c,
        etc. Once downloaded, pass them along for analysis.
        """
        for letter in ascii_lowercase:
            web_page = urllib2.urlopen(self.url + letter).read()
            soup = bs4.BeautifulSoup(web_page ,'lxml')
            self.scrape_courses(soup)

    def scrape_courses(self, soup):
        """
        Parses a page of courses under a particular letter and extracts the
        course information.
        :param soup: BeautifulSoup of a web page under a letter.
        """

        # Page layout resembles the following:
        # <h2> -> course category, one of these has multiple courses under it
        # <h3> - > course title
        # <p> -> course description
        # <div class="tablewrap"> -> course details
        # <div class="separator"> -> separates courses

        # We want to start with the first h2 element, then traverse the
        # section by moving on to the next sibling and reacting based on the
        # type of element.

        course = {}
        cur_category = None
        cur_course_name = None
        for element in soup.find(id='simmonsmainBody').children:
            if element.name == 'h2':
                cur_category = element.text
                course['category'] = cur_category
            elif element.name == 'h3':
                course['title'] = element.text
            elif element.name == 'p':
                course['description'] = element.text
            elif (element.name == 'div' and
                    element.attrs == {'class': ['tablewrap']}):
                # Within this element is a table with the following columns:
                # Section, Dates, Days, Times, Room, Instructor,
                # Section Status, Avail Seats, Requires Consent, Credits

                # Sometimes this table has multiple rows for different
                # sections of the course. These should be treated as separate
                # courses for now.
                rows = element.find_all('tr')
                if not rows:
                    continue

                # First row is table headers - skip them
                for row in rows[1:]:
                    cols = row.find_all('td')
                    # if the instructor column has a <br> element, we should join
                    # the names with a ,
                    course['section'], \
                        course['dates'], \
                        course['days'], \
                        course['times'], \
                        course['room'], \
                        course['section status'], \
                        course['avail seats'], \
                        course['requires consent'], \
                        course['credits'] = [c.text.strip() for c in cols
                                             if cols.index(c) != 5]
                    course['instructor'] = ', '.join(
                        [c.string.strip() for c in cols[5].children
                         if isinstance(c, bs4.element.NavigableString)]
                    )
                    course = utils.clean_course(course)
            elif (element.name == 'div' and
                    element.attrs == {'class': ['separator']} and
                    course):
                self.courses.append(course)
                course = {'category': cur_category}


if __name__ == '__main__':
    spider = SimmonsSpider()
    spider.run()
    utils.courses_to_csv(spider.courses, 'simmons_spring_2017.csv')
