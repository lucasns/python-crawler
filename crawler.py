import scrapy
from scrapy.crawler import CrawlerProcess


class ReviewSpider(scrapy.Spider):
    
    def __init__(self, url, user_review = True, output_file = "output"):
        self.name = "rotten crawler"
        self.allowed_domains = ["rottentomatoes.com"]
               
        self.max_pages = 6
        self.max_reviews = 100
        self.max_ratings = 100
        self.url = url + "/reviews/?page=%u"
        self.user_review = user_review
        self.output_file = output_file
           
        if (self.user_review):
            self.url = self.url + "&type=user"
             
        self.start_urls = [self.url % i for i in range(1, self.max_pages+1)]
        
        
    def parse(self, response):
        reviews = []
        ratings = []
        
        if (self.user_review):
            skip = 10
            element = '//div[@class="user_review"]'
        else:
            skip = 4
            element = '//div[@class="the_review"]'
        
        #Review
        
        for sel in response.xpath(element):
            review = str(sel.xpath('text()').extract())
            
            if (self.max_reviews > 0):
                reviews.append(review[skip:len(review)-2])
            else:
                break
            
            self.max_reviews = self.max_reviews - 1
                     
        #Rating
        if (self.user_review == False):    
            for sel in response.xpath('//div[@class="col-xs-16 review_container"]'):
                if (self.max_ratings > 0):
                    string = str(sel.xpath("div[contains(@class, 'review_icon')]").extract())
                    string = string[15: len(string) - 10]
                    if (string == "review_icon icon small fresh"):
                        ratings.append("fresh")
                    elif (string == "review_icon icon small rotten"):
                        ratings.append("rotten")
                    self.max_ratings -= 1;
                else:
                    break
                
                
        else:
            for sel in response.xpath('//div[@class="col-xs-16"]/span[@class="fl"]'):
                if (self.max_ratings > 0):
                    rating = 0
                    if ("xbd" in str(sel.xpath('text()').extract())):
                        rating += 0.5
                    for s in sel.xpath('span[@class="glyphicon glyphicon-star"]'):
                        rating += 1
                    ratings.append(rating)
                    self.max_ratings -= 1;
                else:
                    break
       
                    
        with open(self.output_file + "_reviews.txt", 'a') as f:                
            for i in range(len(reviews)):
                f.write(str(reviews[i]) + "\n")
        
        with open(self.output_file + "_ratings.txt", 'a') as f:                
            for i in range(len(ratings)):
                f.write(str(ratings[i]) + "\n")
                      
        self.crawler.stop()
      
        
def get_reviews(urls):
    for url in urls:
        process = CrawlerProcess()
        process.crawl(ReviewSpider, url, False, url[33:])

    process.start()


#Tests
#urls = ["https://www.rottentomatoes.com/m/finding_dory", "https://www.rottentomatoes.com/m/captain_america_civil_war"]
urls = ["https://www.rottentomatoes.com/m/captain_america_civil_war"]
get_reviews(urls)



