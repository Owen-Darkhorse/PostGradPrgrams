import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class Course(scrapy.Item):
    course_Title = scrapy.Field()
    course_subject = scrapy.Field()
    course_catalog = scrapy.Field()
    unit_weight = scrapy.Field()
    course_component = scrapy.Field()
    grading_basis = scrapy.Field()
    description = scrapy.Field()
    course_ID = scrapy.Field()


class WaterloogradcourseSpider(scrapy.Spider):
    name = 'waterlooGradCourse'
    allowed_domains = ['uwaterloo.ca']
    start_urls = ["https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/ACTSC"]

    # rules = [Rule(LinkExtractor(allow = r'https://uwaterloo.ca/graduate-studies-academic-calendar/node/(\d+)'),\
    #     callback = "parse", follow=True)]
    
    custom_settings = {
        'waterlooGradCcourse.json' : {
            'format' : 'json',
            'overwrite' : True,
            'encoding' : 'utf8'       
        }
        
        }


    def parse(self, response):
        # return {'LinkAnchor' : response.xpath('//div[@class="field-content"]//h2/a')}      
        for linkAnchor in response.xpath('//div[@class="field-content"]//h2/a'):
            course_link = linkAnchor.attrib['href']
            course_page = scrapy.follow(course_link, \
                callback = self.CourseDetails, meta = {'Course' : Course})
            yield course_page


     # Parse the detailed info of a selected course       
    def CourseDetails(Course, response):
        course_Title = response.xpath('//div[@class="uw-site--title"]/h1/text()').get()
        course_subject = response.xpath('//div[contains(@class, "field-name-field-course-subject")]//div[@class="field-item even"]/text()').get()
        course_catalog = response.xpath('//div[contains(@class, "field-name-field-course-catalog-number")]//div[@class="field-item even"]/text()').get()
        unit_weight = response.xpath('//div[contains(@class, "field-name-field-course-units")]//div[@class="field-item even"]/text()').get()
        course_component = response.xpath('//div[contains(@class, "field-name-field-course-component")]//div[@class="field-item even"]/text()').get()
        grading_basis = response.xpath('//div[contains(@class, "field-name-field-course-grading-basis")]//div[@class="field-item even"]/text()').get()
        description = response.xpath('//div[contains(@class, "field-name-field-course-description")]//div[@class="field-item even"]/text()').get()
        course_ID = response.xpath('//div[contains(@class, "field-name-field-course-id")]//div[@class="field-item even"]/text()').get()

        yield {
            'ID' : course_ID,
            'course_Title': course_Title, 'course_subject' : course_subject,
            'course_catalog' : course_catalog, 'unit_weight' : unit_weight,
            'course_component' : course_component, 'grading_basis' :  grading_basis,
            'description' : description
        }
            
# scrapy crawl waterlooGradCourse