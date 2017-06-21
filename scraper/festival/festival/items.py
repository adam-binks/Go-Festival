# -*- coding: utf-8 -*-

import scrapy


class FestivalItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    camping = scrapy.Field()
    description = scrapy.Field()
    pass
