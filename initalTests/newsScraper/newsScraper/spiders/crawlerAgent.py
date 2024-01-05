from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingAgent(CrawlSpider):
    name = "timeForKids"
    allowed_domains = ["timeforkids.com"] 
    start_urls = [
        "https://www.timeforkids.com/g56/"
    ]
    rules = (
        Rule(LinkExtractor(allow=('[^/]+$'))),
    )

    # def parse(self, response):
    #     self.logger.info('Hi, this is an item page! %s', response.url)
    #     item = scrapy.Item()
    #     item['url'] = response.url
    #     return item

class CrawlingAgent(CrawlSpider):
    name = "newsRound"
    allowed_domains = ["bbc.co.uk"] 
    start_urls = [
        "https://www.bbc.co.uk/newsround"
    ]
    rules = (
        Rule(LinkExtractor(allow=('/newsround/[^/]+$'))),
    )