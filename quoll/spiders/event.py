# -*- coding: utf-8 -*-
import scrapy


class Event(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    venue = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    artists = scrapy.Field()
