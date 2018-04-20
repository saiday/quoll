# -*- coding: utf-8 -*-
import scrapy


class IndievoxSpider(scrapy.Spider):
    name = 'indievox'
    allowed_domains = ['indievox.com']
    start_urls = ['https://www.indievox.com/event/ticket/']

    def parse(self, response):
        for event in response.css('div.event-block'):
            yield {
                'title': event.css('div.event-data').xpath('h5/a/@title').extract_first(),
                'info': event.css('div.event-data').xpath('h6/text()').re_first('[\s]{17}(.*)[\s]{12}'),
                'image': event.xpath('a/img/@src').extract_first()
            }