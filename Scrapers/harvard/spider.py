import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.spider import Spider, BaseSpider
from scrapy.http import Request

import logging

import re


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

    def parse_page(self, response):
        """
        Find all links to individual course pages and spin off request to
        parse them.
        """
        pass

    def parse_course(self, response):
        title = response.xpath('//span[@id="detail_title"]/text()').extract()[0]
        print title
