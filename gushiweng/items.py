# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GushiwengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class songciIndexItem(scrapy.Item):
	title = scrapy.Field()		#poem name
	href = scrapy.Field()
	author = scrapy.Field()
	
class songciPoemItem(scrapy.Item):
	title = scrapy.Field()
	score = scrapy.Field()
	dynasty = scrapy.Field()
	author = scrapy.Field()
	poem = scrapy.Field()
	
	translate = scrapy.Field()
	appreciate = scrapy.Field()
	authorInfo = scrapy.Field()