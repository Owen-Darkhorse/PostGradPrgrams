# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CourseObj(scrapy.Item):
    
    course_ID = scrapy.Field()
    course_Title = scrapy.Field()
    course_subject = scrapy.Field()
    course_catalog = scrapy.Field()
    unit_weight = scrapy.Field()
    course_component = scrapy.Field()
    grading_basis = scrapy.Field()
    description = scrapy.Field()
    course_url = scrapy.Field()
    degree = scrapy.Field()
