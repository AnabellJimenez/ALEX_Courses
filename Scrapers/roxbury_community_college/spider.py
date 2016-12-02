import requests
import time
import utils
import bs4
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, \
    NoSuchElementException


class RoxburySpider:


    def __init__(self):
        self.base_url = 'http://www.rcc.mass.edu'
        self.courses = []
        start_url = 'http://www.rcc.mass.edu/course-search?view=search'
        self.browser = webdriver.Firefox()
        self.browser.get(start_url)
        self.pages_visited = {'1'}

    def crawl(self):
        """
        Use the Selenium webdriver (
        http://www.seleniumhq.org/docs/03_webdriver.jsp) to scrape several
        pages of the Roxbury course list.

        Selenium is necessary because the pagination on the courses table is
        actually done through javascript, not fixed urls. So we need to
        simulate actually clicking on the page items.

        This function is responsible for following the pagination links and
        calling the other function, which does the actual scraping.
        """

        # Scrape the courses from this page first.
        self.scrape_courses()

        # Now follow the first pagination link that hasn't been crawled yet.
        page_links = self.browser.find_elements_by_xpath(
            '//ul[@class="pagination-list"]/li/a')
        link_to_follow = None

        for link in page_links:
            if link.text and link.text not in self.pages_visited:
                print '-- About to crawl {}'.format(link.text)
                link_to_follow = link
                break

        if link_to_follow is None:
            print 'Finished scraping. {}'.format(self.pages_visited)
            return

        self.pages_visited.add(link_to_follow.text)
        link_to_follow.click()

        # Wait for the page to load
        # i.e. the old link is stale and the admin form is on the page
        def page_has_loaded():
            try:
                l = link_to_follow.text
                return False
            except StaleElementReferenceException:
                try:
                    self.browser.find_element_by_id('adminForm')
                    return True
                except NoSuchElementException:
                    print 'no element yet'
                    return False

        t1 = time.time()
        while time.time() < t1 + 5:
            if page_has_loaded():
                return self.crawl()
            else:
                time.sleep(0.1)
        raise Exception('Waited to long for {}'.format(link_to_follow.text))

    def scrape_courses(self):
        """
        Scrape the course table on the current browser page.
        Also, make a request to scrape the description from the course detail
        page as well.
        """
        # Skip the first row cause its a header row.
        rows = self.browser.find_elements_by_xpath('//table/tbody/tr')[1:]

        # Each row has 4 column.
        # Course (link to detail) | Category | Title | Credits
        for row in rows:
            abbrev, category, title, credits = row.find_elements_by_tag_name(
                'td')
            course_link = abbrev.find_element_by_tag_name('a')
            # filter out fake rows
            if abbrev.text == 'category':
                continue
            resp = requests.get(course_link.get_attribute('href'))
            soup = bs4.BeautifulSoup(resp.text, 'lxml')
            desc = soup.select('div.location-result p')[0]

            course = {
                'course': abbrev.text.upper(),
                'title': title.text.title(),
                'category': category.text.title(),
                'credits': credits.text,
                'description': desc.text
            }
            final = utils.clean_course(course)
            print final['course'], '-', final['title']
            self.courses.append(utils.clean_course(final))

if __name__ == '__main__':
    spider = RoxburySpider()
    spider.crawl()
    utils.courses_to_csv(spider.courses, 'roxbury_community_college.csv')
