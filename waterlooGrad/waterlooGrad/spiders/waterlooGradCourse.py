import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WaterloogradcourseSpider(scrapy.Spider):
    name = 'waterlooGradCourse'
    allowed_domains = ['uwaterloo.ca']
    start_urls = ["https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/ACTSC"]

    rules = [Rule(LinkExtractor(allow = r'https://uwaterloo.ca/graduate-studies-academic-calendar/node/(\d+)'),\
        callback = "parse", follow=True)]

    def parse(self, response):
        # course_ID = response.xpath('//div[@class="field-content"]/div[@class="course_id"]/text()').get()
        # course_Code = response.xpath('//div[@class="field-content"]//h2/a[name="611"]/text()').get()
        # course_Title = response.xpath('//div[@class="field-content"]//h2/a/text()').get()
        # course_des = response.xpath('//div[@class="field-content"]/div[@class="course_des"]/text()').get()

        for linkAnchor in response.xpath('//div[@class="field-content"]//h2/a'):
            course_link = linkAnchor.attrib['href']
            course_page = scrapy.Request(course_link)

            
            course_Title = response.xpath('//div[@class="uw-site--title"]/h1/text()').get()
            # course_ID = response.xpath('//div[@class="field-content"]/div[@class="course_id"]/text()').get()
            # course_Code = response.xpath('//div[@class="field-content"]//h2/a[name="611"]/text()').get()
            # course_des = response.xpath('//div[@class="field-content"]/div[@class="course_des"]/text()').get()
            # return {
            #         "ID": course_ID, "Code": course_Code, "Title": course_Title,\
            #         "Description": course_des
            # }

# scrapy crawl waterlooGradCourse
# '//*[@id="block-system-main"]/div/div/div[2]/div[1]/div/div/h2/a[1]'