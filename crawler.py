import scrapy
from scrapy.crawler import CrawlerProcess


class ReviewSpider(scrapy.Spider):
    
    def __init__(self, url, user_review = True, output_file = "output.txt"):
        self.name = "rotten crawler"
        self.allowed_domains = ["rottentomatoes.com"]
               
        self.max_pages = 6
        self.max_reviews = 100
        self.url = url + "/reviews/?page=%u"
        self.user_review = user_review
        self.output_file = output_file
           
        if (self.user_review):
            self.url = self.url + "&type=user"
             
        self.start_urls = [self.url % i for i in range(1, self.max_pages+1)]
        
        
    def parse(self, response):
        if (self.user_review):
            skip = 10
            element = '//div[@class="user_review"]'
        else:
            skip = 4
            element = '//div[@class="the_review"]'
        
        with open(self.output_file, 'a') as f:
            for sel in response.xpath(element):
                review = str(sel.xpath('text()').extract())
                
                if (self.max_reviews > 0):
                    f.write(review[skip:len(review)-2] + "\n")
                else:
                    break
                
                self.max_reviews = self.max_reviews - 1
            
                
        self.crawler.stop()
        
        
def get_reviews(urls):
    for url in urls:
        process = CrawlerProcess()
        process.crawl(ReviewSpider, url, False, url[33:]+".txt")

    process.start()


#Tests
urls = ["https://www.rottentomatoes.com/m/finding_dory", "https://www.rottentomatoes.com/m/captain_america_civil_war"]
get_reviews(urls)



