import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json

class CrawlingAgent(CrawlSpider):
    name = "newsRound"
    allowed_domains = ["bbc.co.uk"]
    start_urls = ["https://www.bbc.co.uk/newsround"]
    rules = (
        Rule(LinkExtractor(allow=('/newsround/[6-9]{2}\d*$')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        article_name = response.xpath('//h1/text()').get() or response.css('h1::text').get()
        article_content = ' '.join(response.xpath('//p/text()').getall())
        if article_name and article_content:
            article_id = int(re.findall(r'\d+$', response.url)[0])
            return {
                'id': article_id,
                'name': article_name.strip(),
                'content': article_content.strip()
            }

def run_crawler():
    if os.path.exists('../data/output.json'):
        os.remove('../data/output.json')
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': '../data/output.json',
        'LOG_LEVEL': 'INFO',
        'CLOSESPIDER_ITEMCOUNT': 10
    })
    process.crawl(CrawlingAgent)
    process.start()

def fetch_news():
    run_crawler()
    try:
        with open('../data/output.json', 'r') as file:
            news_data = json.load(file)
        return news_data
    except FileNotFoundError:
        return {"error": "News data not found"}

fetch_news()