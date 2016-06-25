import scrapy
from scrapy.crawler import CrawlerProcess


class ReviewSpider(scrapy.Spider):
    
    def __init__(self, url, max_pages = 6, max_reviews = 100):
        self.name = "rotten crawler"
        self.allowed_domains = ["rottentomatoes.com"]
        
        self.url = url
        self.max_pages = 6
        self.max_reviews = 100
        
        self.start_urls = [self.url % i for i in range(1, self.max_pages+1)]
        
        
    def parse(self, response):
        with open("output.txt", 'a') as f:
            for sel in response.xpath('//div[@class="user_review"]'):
                review = sel.xpath('text()').extract()
                f.write(str(review)+"\n")
                self.max_reviews = self.max_reviews - 1
                
                if (self.max_reviews <= 0):
                    break
   
   
        self.crawler.stop()
        
def get_reviews(urls):
    for url in urls:
        process = CrawlerProcess()
        process.crawl(ReviewSpider, url)

    process.start()

urls = ["https://www.rottentomatoes.com/m/finding_dory/reviews/?page=%u&type=user&sort="]
getReviews(urls)



