import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css(
            'section#numerical-index tbody a::attr(href)')
        for pep_link in pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        page_title = response.css('h1.page-title::text').get()
        pattern = r'PEP (?P<number>\d+)\W+(?P<name>.+)'
        number, name = re.search(pattern, page_title).groups()
        data = {
            'number': number,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text').get(),
        }
        yield PepParseItem(data)
