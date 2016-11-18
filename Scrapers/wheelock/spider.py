import re

import utils

import scrapy
from scrapy.spiders import CrawlSpider, Rule

URL = 'http://www.wheelock.edu'


class WheelockSpider(CrawlSpider):

    name = 'wheelock'

    start_urls = [
        ('http://www.wheelock.edu/academics/academic-records-and-registration'
         '/course-catalog')
    ]

    def parse(self, response):
        """
        Find all department links, spin off requests to parse each one
        """
        department_links = response.xpath(
            '//div[@id="contentLeft"]/ul[6]/li/a/@href'
        )
        for link in department_links:
            yield scrapy.Request(URL + link.extract(),
                                 callback=self.parse_department)

    def parse_department(self, response):
        courses = []

        headers = response.xpath('//p[@class="Heading-6-Courses"]/strong')
        bodies = response.xpath('//p[@class="Course-Body"]/text()')

        assert len(headers) == len(bodies)

        for i in range(len(headers)):
            head = headers[i]
            body = bodies[i].extract()

            head_split = head.extract().split('<br>')
            prefix, title, creds = [re.sub(r'<(.*?)>', '', s).strip()
                                    for s in head_split]
            print '------'
            print prefix, ':', title, '(', creds, ')'
            creds = re.sub(r' [cC]{1}redit[s]{0,1}(.*?)$', '', creds)
            creds = re.sub(r'[ ]{0,1}\-[ ]{0,1}', ' to ', creds)

            course = {
                'title': '{}: {}'.format(prefix, title),
                'credits': creds,
                'body': body
            }
            yield utils.clean_course(course)
