import re

import utils
import bs4
import urllib2


class MassArtSpider:


    base_url = 'http://academic-catalog.massart.edu'
    courses = []
    course_set = set()

    def crawl(self, page_num, url):
        print page_num
        web_page = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(web_page, 'lxml')

        # The page structure looks like this:
        # form id=course_search
        # + table
        # > tr for each course
        #   > a links to course description page
        # > final tr is pagination links
        form = soup.find('form', {'id': 'course_search'})
        table = form.find_next_sibling()
        rows = table.find_all('tr')
        print '----', len(rows)
        category = None
        for row in rows[:-1]:
            if len(row.contents) == 3:
                # This is a catgeory
                category = row.text.strip().encode('ascii', 'ignore')
            elif len(row.contents) > 3:
                # This is a course
                # print len(row.contents)
                self.scrape_course(row, category)
            else:
                pass

        # Just follow the next page numerically
        footer = rows[-1].find('td')
        links = [l for l in footer.contents if l.name == 'a']
        for l in links:
            if int(l.text) > page_num:
                new_url = '{}{}'.format(self.base_url, l.attrs['href'])
                return self.crawl(int(l.text), new_url)

    def scrape_course(self, row, category):
        course = {}
        info = row.find('a')
        title = info.text
        credits = re.search(r'(\d)\s?cr', title)
        if credits:
            course['credits'] = credits.group(0).replace('cr', '').strip()
            course['title'] = title.replace(credits.group(0), '').strip()
        else:
            course['credits'] = None
            course['title'] = title
        course['category'] = category
        course['link'] = '{}/{}'.format(self.base_url, info.attrs['href'])

        desc_page = urllib2.urlopen(course['link']).read()
        soup = bs4.BeautifulSoup(desc_page, 'lxml')
        td = soup.find('td', {'class': 'block_content'})
        # We need to be smart about how we grab the description cause its not
        # very organized.
        # We only want elements that contain description text.
        desc = []
        for i, c in enumerate(td.contents):
            if c.name in ('h1', 'table', 'div'):
                pass
            elif c.name == 'br' and td.contents[i + 1].name == 'br':
                break
            else:
                if isinstance(c, bs4.element.NavigableString):
                    text = c.string
                else:
                    text = c.text
                desc.append(text.strip().encode('ascii', 'ignore'))

        # desc = [c.string.strip().encode('ascii','ignore') for c in td.contents
        #         if isinstance(c, bs4.element.NavigableString) and
        #         c.string.strip().encode('ascii','ignore')]
        course['description'] = ' '.join(desc).replace(' ,', ',').strip()
        print course['title'], ':', course['credits']
        self.courses.append(utils.clean_course(course))


if __name__ == '__main__':
    spider = MassArtSpider()
    start_url = ('http://academic-catalog.massart.edu/content.php?catoid=6&'
                 'catoid=6&navoid=148&filter%5B27%5D=-1&filter%5B29%5D=&fil'
                 'ter%5Bcourse_type%5D=-1&filter%5Bkeyword%5D=&filter%5B32%'
                 '5D=1&filter%5Bcpage%5D=1&filter%5Bexact_match%5D=1&filter'
                 '%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D'
                 '=1')
    spider.crawl(1, start_url)
    utils.courses_to_csv(spider.courses, 'massart.csv')
