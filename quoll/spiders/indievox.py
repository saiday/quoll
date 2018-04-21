# -*- coding: utf-8 -*-
import scrapy

from quoll.spiders.event import Event


class IndievoxSpider(scrapy.Spider):
    name = 'indievox'
    allowed_domains = ['indievox.com']
    start_urls = ['https://www.indievox.com/event/ticket/']

    def parse(self, response):
        for event in response.css('div.event-block'):
            detail = event.css('div.event-data').xpath('a/@href').extract_first()
            title = event.css('div.event-data').xpath('h5/a/@title').extract_first()
            image = event.xpath('a/img/@src').extract_first()
            meta = {'processing_event': Event(title=title, image=image)}
            yield response.follow(detail, self.parse_detail, meta=meta)

    def parse_detail(self, response):
        event = response.meta['processing_event']

        event['body'] = response.css('h1+ div').extract_first()  # html body

        # \n                                            2018/04/21(Sat) 19:30
        event['date'] = response.css('tr:nth-child(2) td::text')[0].re_first('[\s]{44}(\d{4}\/\d{2}\/\d{2})')
        event['time'] = response.css('tr:nth-child(2) td::text')[0].re_first('(\d{2}\:\d{2})')
        event['venue'] = response.css('tr:nth-child(5) td a::text').re_first('\s{53}(.*)\s{48}')
        event['address'] = response.css('tr:nth-child(6) td::text').re_first('\s{97}(.*)')
        event['price'] = response.css('tr:nth-child(1) td::text').re_first('\s{45}(.*)\s{40}')

        # might have <a> and raw text element inside artist <td>
        linked_artists = response.css('tr:nth-child(3) td a::text').extract()
        unlinked_artists = response.css('tr:nth-child(3) td::text').re('\w{2,}')
        event['artists'] = linked_artists + unlinked_artists

        yield dict(event)
