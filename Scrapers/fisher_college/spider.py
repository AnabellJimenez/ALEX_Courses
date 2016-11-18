import utils

import scrapy
from scrapy.spiders import CrawlSpider


class FisherCollegeSpider(CrawlSpider):

    url = 'http://www.fisher.edu'
    name = 'fisher'
    start_urls = [
        ('http://www.fisher.edu/academics/catalogs/course-descriptions')
    ]

    def parse(self, response):
        """
        Parse the starting page to find all links to categories, then follow
        them and pass new page to another callback.
        """
        category_links = response.xpath(
            '//div[@id="TS_D_G_Guide1Ajax"]/div/table/tbody/tr/td/table/tbody'
            '/tr/td/span/ul/li/a/@href'
        )
        for c in category_links:
            link = c.extract()
            if not link.startswith('http'):
                link = self.url + link
            yield scrapy.Request(link, callback=self.parse_category_page)


    def parse_category_page(self, response):
        """
        Parse the page for a particular category and find all links to
        individual course pages, then follow them and pass new page to
        another callback.
        """
        course_links = response.xpath(
            '//div[@id="TS_D_G_Guide1Ajax"]/div/table/tbody/tr/td/table'
            '/tbody/tr/td/a/@href'
        )
        for c in course_links:
            link = c.extract()
            if not link.startswith('http'):
                link = self.url + link
            yield scrapy.Request(link, callback=self.parse_course)

        # Some of these pages have a "Next >" option to follow as well.
        next_page = response.xpath('//a[@id="TS_D_G_ctl18_BTnext"]/@href')
        if next_page:
            link = next_page.extract()[0]
            if not link.startswith('http'):
                link = self.url + link
            yield scrapy.Request(link, callback=self.parse_category_page)

    def parse_course(self, response):
        """
        Scrape the contents for an individual course.
        """
        course = {}
        course['title'] = response.xpath(
            '//h1/a[@class="title"]/text()'
        ).extract()[0]
        course['category'] = response.xpath(
            '//div[@class="Breads"]/span/text()'
        ).extract()[0]

        # The description element manifests differently on every course page!
        desc_all = response.xpath(
            '//span[@class="text"]/descendant-or-self::*/text()'
        )
        # Filter line breaks and other random artifacts.
        desc_extracted = [c.extract().strip().replace('\r\n', '').encode(
                          'ascii', 'ignore') for c in desc_all]
        # Filter out known unnecessary information.
        desc_filtered = [c for c in desc_extracted[:-1]
                         if 'Credit Hours' not in c
                         and 'Course Descriptions' not in c
                         and c != course['title']
                         and c != '']
        # Separate out prerequisites, if there are any.
        prerequisites = [c for c in desc_filtered
                         if c.startswith('Prerequisite')]
        if prerequisites:
            course['prerequisite'] = prerequisites[0]
            desc_filtered.remove(course['prerequisite'])
        else:
            course['prerequisite'] = None
        course['description'] = '; '.join(desc_filtered)
        print course['title']
        yield utils.clean_course(course)
