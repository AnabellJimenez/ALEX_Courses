import urllib2

import time

import utils
import bs4
import re
from string import ascii_lowercase


class LesleySpider:

    base_url = 'http://lesley.smartcatalogiq.com'
    courses = []
    fields = {'title', 'description', 'credits', 'college', 'department'}

    def run(self):

        art_and_design = (
            'http://lesley.smartcatalogiq.com/en/2016-2017/Undergraduate-Acade'
            'mic-Catalog/Undergraduate-Catalog/College-of-Art-and-Design-Cours'
            'es'
        )
        web_page = urllib2.urlopen(art_and_design).read()
        soup = bs4.BeautifulSoup(web_page, 'lxml')
        self.scrape_department(soup, 'College of Art and Design')

        liberal_and_science = (
            'http://lesley.smartcatalogiq.com/en/2016-2017/Undergraduate-Acade'
            'mic-Catalog/Undergraduate-Catalog/College-of-Liberal-Arts-and-Sci'
            'ences-Courses'
        )
        web_page = urllib2.urlopen(liberal_and_science).read()
        soup = bs4.BeautifulSoup(web_page, 'lxml')
        self.scrape_department(soup, 'College of Liberal Arts and Sciences')

    def scrape_department(self, soup, college):
        """
        Find all department links and pass each one along to scrape_courses.
        """
        links = soup.select('ul.sc-child-item-links li a')
        for link in links:
            department = link.text.strip()
            url = '{}{}'.format(self.base_url, link.attrs['href'])
            web_page = urllib2.urlopen(url).read()
            new_soup = bs4.BeautifulSoup(web_page, 'lxml')
            self.scrape_courses(new_soup, college, department)

    def scrape_courses(self, soup, college, department):
        """
        Find all course links and pass each one along to scrape_course
        """
        links = soup.select('#main > ul li a')
        for link in links:
            url = '{}{}'.format(self.base_url, link.attrs['href'])
            web_page = urllib2.urlopen(url).read()
            new_soup = bs4.BeautifulSoup(web_page, 'lxml')
            self.scrape_course(new_soup, college, department)

    def scrape_course(self, soup, college, department):
        course = {}
        section = soup.select('#main')[0]
        title = section.find('h1')
        description = section.find('div', {'class': 'desc'})
        credits = section.find('div', {'class': 'credits'})
        others = section.find_all('h3')
        others.pop(0)
        if others:
            indices = [(h3, section.contents.index(h3)) for h3 in others
                       if h3 in section.contents]
            for i, (h3, h3_index) in enumerate(indices):
                if i == len(indices) - 1:
                    end = len(section.contents)
                else:
                    end = indices[i + 1][1]
                if h3_index == end - 1:
                    contents = [section.contents[end]]
                else:
                    contents = section.contents[h3_index + 1: end]
                final_contents = []
                for c in contents:
                    if isinstance(c, bs4.element.NavigableString):
                        final_contents.append(c.string.strip())
                    elif c.name == 'div':
                        pass
                    else:
                        final_contents.append(c.text.strip())
                field = h3.text.strip().encode('ascii', 'ignore')
                self.fields.add(field)
                course[field] = ' '.join(final_contents)

        course['college'] = college
        course['department'] = department
        course['title'] = title.text.strip()
        course['description'] = description.text.strip()
        course['credits'] = credits.text.strip() if credits else None
        print course['title']
        self.courses.append(utils.clean_course(course))


if __name__ == '__main__':
    spider = LesleySpider()
    t1 = time.time()
    spider.run()
    print time.time() - t1, 'seconds'
    utils.courses_to_csv(spider.courses, 'lesley.csv', spider.fields)
