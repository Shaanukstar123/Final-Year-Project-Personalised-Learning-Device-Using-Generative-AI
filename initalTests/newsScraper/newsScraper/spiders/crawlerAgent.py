from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

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
        Rule(LinkExtractor(allow=('/newsround/[6-9]{2}\d+$')), callback='parse_item'), #filters latest news (needs to be made dynamic later e.g. full scan and get largest ID then subtract 30)
    )
    def __init__(self, *args, **kwargs):
        super(CrawlingAgent, self).__init__(*args, **kwargs)
        self.article_links = []

    def parse_item(self, response):
        # Extract the numeric ID from the URL
        numeric_id = int(response.url.split('/')[-1])
        # Store the URL and the numeric ID
        self.article_links.append((numeric_id, response.url))

    def closed(self, reason):
        # Sort the collected links based on their numeric ID in descending order
        self.article_links.sort(reverse=True, key=lambda x: x[0])
        # Select the top 30 newest articles
        top_30_links = self.article_links[:30]
        # Process the top 30 links as you see fit
        for link in top_30_links:
            print(f"Article ID: {link[0]}, URL: {link[1]}")

# Main runner
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CrawlingAgent)
    process.start()