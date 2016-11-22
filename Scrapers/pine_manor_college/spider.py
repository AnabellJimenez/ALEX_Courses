import urllib2
import utils
import bs4
import re
from string import ascii_lowercase


class PineManorCollegeSpider:

    base_url = 'http://www.pmc.edu'
    courses = []

    def run(self):
        """
        Download each of the web pages in the category index.
        Once downloaded, pass them along for analysis.
        """
        url = '{}/course-descriptions'.format(self.base_url)
        web_page = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(web_page, 'lxml')
        links = soup.select('#sec-nav a')
        for link in links:
            final = self.base_url + link.attrs['href']
            web_page = urllib2.urlopen(final).read()
            soup = bs4.BeautifulSoup(web_page ,'lxml')
            self.scrape_courses(soup)

    def scrape_courses(self, soup):
        """
        This site is a mess!
        """

        section = soup.find('div', {'id': 'MainContent_0_0_pnlDiv'})
        if section is None:
            return
        items = section.find_all('p')
        for item in items:
            all_text = []
            for s in item.children:
                if isinstance(s, bs4.element.NavigableString):
                    cleaned = s.string.encode('ascii', 'ignore').strip()
                    all_text.append(cleaned)
                else:
                    for a in s.contents:
                        if isinstance(a, bs4.element.NavigableString):
                            cleaned = a.string.encode('ascii', 'ignore').strip()
                            all_text.append(cleaned)
                        else:
                            text = [c.string.encode('ascii', 'ignore').strip()
                                    for c in a.contents
                                    if isinstance(c, bs4.element.NavigableString)]
                            all_text.append(': '.join(text))
            all_text = [a for a in all_text if a]
            if all_text:
                course = {}
                if len(all_text) > 2:
                    t1, t2 = all_text[:2]
                    course['title'] = '{}: {}'.format(t1, t2)
                    all_text = all_text[2:]
                else:
                    course['title'] = all_text.pop(0)
                course['desc'] = ''.join(all_text)
                self.courses.append(utils.clean_course(course))


if __name__ == '__main__':
    spider = PineManorCollegeSpider()
    spider.run()
    utils.courses_to_csv(spider.courses, 'pine_manor_college.csv')
