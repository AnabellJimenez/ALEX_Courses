import utils

import scrapy
from scrapy.spiders import CrawlSpider, Rule

URL = 'https://courses.harvard.edu/'


class HarvardSpider(CrawlSpider):

    name = 'harvard'

    start_urls = [
        ('https://courses.harvard.edu/search?fq_coordinated_semester_yr'
         '=coordinated_semester_yr%3A%22Jan+to+May+2017+%28Spring+Term%29%22'
         '&fq_school_nm=&q=&sort=course_title+asc&start=0&submit=Search')
    ]

    def parse(self, response):
        """
        On every search page:
        1. Find all course detail links, spin off requests to parse each one
        2. Find next page link, spin off request to parse
        """
        print response._url[-22:]
        course_detail_links = response.xpath('//span['
                                             '@class="course_title"]/a/@href')
        for link in course_detail_links:
            yield scrapy.Request(URL + link.extract(),
                                 callback=self.parse_course)

        try:
            next_page = response.xpath('//span[@class="prevnext"]/a/@href')[-1]
        except IndexError:
            print 'DONE'
            return

        yield scrapy.Request(URL + next_page.extract(), callback=self.parse)


    def parse_course(self, response):
        course = {}

        course['title'] = response.xpath(
            '//span[@id="detail_title"]/text()'
        ).extract()[0]

        course['description'] = response.xpath(
            '//p[@id="detail_description"]/text()'
        ).extract()[0]

        # There are 5 tables on every course page
        # the interesting data is in the second row of each table
        tables = response.xpath('//div[@id="detail"]/table')

        # Table 1: School, Department, Faculty
        row1_cols = tables[0].xpath('tr[2]/td')
        course['school'] = row1_cols[0].xpath('text()').extract()[0]
        course['department'] = row1_cols[1].xpath('text()').extract()[0]
        course['faculty'] = row1_cols[2].xpath('span/text()').extract()[0]

        # Table 2: Term, Day and Time
        row2_cols = tables[1].xpath('tr[2]/td')
        course['term'] = row2_cols[0].xpath('text()').extract()[0]
        # day and time has some weird spacing, fix it
        day_and_time_raw = row2_cols[1].xpath('text()').extract()[0]
        day_and_time_raw = [s.encode('ascii', 'ignore')
                            for s in day_and_time_raw.split('\t')
                            if s]
        course['day_and_time'] = ' '.join(day_and_time_raw)

        # Table 3: Credits, Credit Level
        row3_cols = tables[2].xpath('tr/td')
        course['credits'] = row3_cols[0].xpath('text()').extract()[0]
        course['credit_level'] = row3_cols[1].xpath('text()').extract()[0]

        # self.course_list.append(utils.clean_course(course))
        # self.courses[course['title']] = course
        final = utils.clean_course(course)
        final['url'] = response._url
        yield final

        # Table 4: Textbook info, skip
        # Table 5: Cross Registration, skip
