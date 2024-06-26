import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
import os
import time

class CrawlingAgent(CrawlSpider):
    name = "newsRound"
    allowed_domains = ["bbc.co.uk"]
    start_urls = ["https://www.bbc.co.uk/newsround"]
    scraped_data = []

    rules = (
    Rule(LinkExtractor(allow=r'/newsround/[6-9]\d*$'), callback='parse_item', follow=True),
    # example: https://www.bbc.co.uk/newsround/61179377
    )


    def parse_item(self, response):
        article_name = response.xpath('//h1/text()').get() or response.css('h1::text').get()
        article_content = ' '.join(response.xpath('//p/text()').getall())
        if article_name and article_content:
            article_id = int(re.findall(r'\d+$', response.url)[0])
            data = {
                'id': article_id,
                'name': article_name.strip(),
                'content': article_content.strip()
            }
            self.scraped_data.append(data)
            return data

def run_crawler():
    # Remove existing output.json if it exists
    output_file = 'data/output.json'
    if os.path.exists(output_file):
        os.remove(output_file)
        
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': output_file,
        'LOG_LEVEL': 'INFO',
        'CLOSESPIDER_ITEMCOUNT': 30
    })
    process.crawl(CrawlingAgent)
    process.start()

def fetch_news():
    run_crawler()

    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        if os.path.exists('data/output.json'):
            try:
                with open('data/output.json', 'r') as file:
                    news_data = json.load(file)
                if news_data:
                    return news_data
                else:
                    print("No data found in the JSON file. Retrying...")
            except FileNotFoundError:
                print("FileNotFoundError occurred while attempting to read the file. Retrying...")
        else:
            print("Output file not found. Waiting for it to be created...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            retry_count += 1

    return {"error": "News data not found after multiple retries"}

fetch_news()
