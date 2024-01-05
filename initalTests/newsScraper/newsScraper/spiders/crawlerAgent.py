import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

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
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
class CrawlingAgent(CrawlSpider):
    name = "newsRound"
    allowed_domains = ["bbc.co.uk"] 
    start_urls = ["https://www.bbc.co.uk/newsround"]
    
    rules = (
        Rule(LinkExtractor(allow=('/newsround/[6-9][6-9]\d*$')), callback='collect_links'),
    )

    def __init__(self, *args, **kwargs):
        super(CrawlingAgent, self).__init__(*args, **kwargs)
        self.article_links = []

    def parse_article(self, response):
        print("Entered parse_article")  # Debug: Confirm entering the method
        item = ArticleItem()
        item['title'] = response.xpath('//h1/text()').get()  # Update this XPath according to the site's structure
        item['text'] = response.xpath('//div[@class="article-text"]/p//text()').get()  # Update this XPath
        print("Parsed article:", item['title'])  # Debug: Print the title
        yield item

    def collect_links(self, response):
        # Collecting links
        numeric_id = int(response.url.split('/')[-1])
        self.article_links.append((numeric_id, response.url))
        
        # Once enough links are collected, sort and yield requests for top 30 articles
        if len(self.article_links) >= 30:  
            self.article_links.sort(reverse=True, key=lambda x: x[0])
            top_30_links = self.article_links[:30]

            for _, url in top_30_links:
                print("Yielding request for:", url)
                yield Request(url, callback=self.parse_article)

# Main runner
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "articles.json": {"format": "json"},
        },
    })
    process.crawl(CrawlingAgent)
    process.start()