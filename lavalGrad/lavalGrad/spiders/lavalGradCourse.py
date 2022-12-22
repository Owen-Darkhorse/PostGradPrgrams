import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from lavalGrad.items import CourseObj

MActSc_catalog = [611, 612, 613, 614, 615, 621, 622, 623, 624, 625, 631, 632, 633, 634, 635]
MQF_ActSc_catalog = [770, 771, 772, 974]
MMath_ActSc_catalog = [845, 846, 895, 855, 962, 964, 970, 974]

MQF_STAT_catalog = [850, 901, 902, 906, 974]
MMath_STAT_catalog = [831, 840, 841, 906]
AVIA_catalog = [601, 602]
GEOG_catalog = [600, 620, 640, 660]
ERS_catalog = [680, 681, 669]

search_groups = {
    'MActSc': {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/ACTSC",
        'Catalog' : MActSc_catalog,
        'Degree' : "Master of Acturial Science"
    } ,
    'MQF_ActSc_catalog' : {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/ACTSC",
        'Catalog' : MQF_ActSc_catalog,
        'Degree' : "Master of Quantative Finance"
    },
    'MMath_ActSc_catalog' : {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/ACTSC",
        'Catalog' : MMath_ActSc_catalog,
        'Degree' : "Master of Mathematics in Acturial Science"
    },
    'MQF_STAT': {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/STAT",
        'Catalog' : MQF_STAT_catalog,
        'Degree' : "Master of Quantative Finance"
    } ,
    'MMath_STAT': {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/STAT",
        'Catalog' : MMath_STAT_catalog,
        'Degree' : "Master of Mathematics in Acturial Science"
    } ,
    'AVIA': {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/AVIA",
        'Catalog' : AVIA_catalog,
        'Degree' : "Master of Environmental Studies in Georgraphy - Aeronnautics"
    } ,
    'GEOG': {
        'URL': "https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/GEOG",
        'Catalog' : GEOG_catalog,
        'Degree' : "Master of Environmental Studies in Georgraphy - Aeronnautics"
    } ,
    'ERS': {
        'URL': 'https://uwaterloo.ca/graduate-studies-academic-calendar/graduate-course/subject/ERS',
        'Catalog' : ERS_catalog,
        'Degree' : "Master of Environmental Studies in Social And Ecological Sustainability"
        }

}

class LavalgradcourseSpider(scrapy.Spider):
    name = 'lavalGradCourse'
    allowed_domains = ['laval.ca']
    # start_urls = search_groups

    # rules = [Rule(LinkExtractor(allow = r'https://uwaterloo.ca/graduate-studies-academic-calendar/node/(\d+)'),\
    #     callback = "parse", follow=True)]
    
    def start_requests(self):
        start_urls = search_groups

        for key in start_urls:
            group_info = start_urls[key]
            URL = group_info["URL"]
            Catalog= group_info["Catalog"]
            Degree = group_info['Degree']

            # print(group_info)
            request = scrapy.Request(url = URL, callback = self.parse,\
                cb_kwargs={'allowedCatalog':Catalog, 'Degree' : Degree})
            yield request


    def parse(self, response, allowedCatalog, Degree):
        for linkAnchor in response.xpath('//li//div[contains(@class, "cours-carte")]/a[@class="carte-accessible--lien"]'):
            course_link = linkAnchor.attrib['href']
            # yield {'LinkAnchor' : course_link, 'type' : type(course_link)}      
            course_page = response.follow(course_link, callback = self.CourseDetails, \
                    cb_kwargs = {'allowedCatalog' : allowedCatalog, 'Degree' : Degree})
            
            yield course_page #, callback = self.CourseDetails

     # Parse the detailed info of a selected course       
    def CourseDetails(self, response, allowedCatalog, Degree):
        testCatalog = response.xpath('//div[contains(@class, "field-name-field-course-catalog-number")]//div[@class="field-item even"]/text()').get()
        if int(testCatalog) in allowedCatalog:
            Course = CourseObj()
            Course['course_Title'] = response.xpath('//div[@class="uw-site--title"]/h1/text()').get()
            Course['course_subject'] = response.xpath('//div[contains(@class, "field-name-field-course-subject")]//div[@class="field-item even"]/text()').get()
            Course['course_catalog'] = response.xpath('//div[contains(@class, "field-name-field-course-catalog-number")]//div[@class="field-item even"]/text()').get()
            Course['unit_weight'] = response.xpath('//div[contains(@class, "field-name-field-course-units")]//div[@class="field-item even"]/text()').get()
            Course['course_component'] = response.xpath('//div[contains(@class, "field-name-field-course-component")]//div[@class="field-item even"]/text()').get()
            Course['grading_basis'] = response.xpath('//div[contains(@class, "field-name-field-course-grading-basis")]//div[@class="field-item even"]/text()').get()
            Course['description'] = response.xpath('//div[contains(@class, "field-name-field-course-description")]//div[@class="field-item even"]/text()').get()
            Course['course_ID'] = response.xpath('//div[contains(@class, "field-name-field-course-id")]//div[@class="field-item even"]/text()').get()
            Course['course_url'] = response.url
            Course['degree'] = Degree
            yield Course

        # yield {'testCata' : int(testCatalog)}

        # yield {"Title" :  response.xpath('//div[@class="uw-site--title"]/h1/text()').get()}
            
# scrapy crawl waterlooGradCourse