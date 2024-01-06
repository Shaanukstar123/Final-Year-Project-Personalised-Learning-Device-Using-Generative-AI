import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingAgent(CrawlSpider):
    name = "newsRound"
    allowed_domains = ["bbc.co.uk"]
    start_urls = ["https://www.bbc.co.uk/newsround"]

    # Setting up a rule to allow scraping in the specific article structure
    rules = (
        Rule(LinkExtractor(allow=('/newsround/[6-9]{2}\d*$')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # Extract article content using XPath or CSS selectors
        # Assuming article titles are within <h1> tags and contents within <p> tags
        article_name = response.xpath('//h1/text()').get() or response.css('h1::text').get()
        article_content = ' '.join(response.xpath('//p/text()').getall())

        # Only proceed if both name and content could be found
        if article_name and article_content:
            article_id = int(re.findall(r'\d+$', response.url)[0])  # Extracts ID from URL
            return {
                'id': article_id,
                'name': article_name.strip(),
                'content': article_content.strip()
            }

# The main execution
if __name__ == "__main__":
    # Set up the crawler and start it
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',           # Set format of the output file
        'FEED_URI': 'output.json',       # Name of the output file
        'LOG_LEVEL': 'INFO',             # Set logging level
        'CLOSESPIDER_ITEMCOUNT': 10      # Close spider after scraping 10 items
    })

    process.crawl(CrawlingAgent)
    process.start()  # the script will block here until the crawling is finished
