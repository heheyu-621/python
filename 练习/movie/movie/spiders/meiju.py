import scrapy
from movie.items import MovieItem
class MeijuSpider(scrapy.Spider):
    name = "meiju"
    allowed_domains = ["books.com"]
    start_urls = ["http://books.toscrape.com/catalogue/category/books/travel_2/index.html"]
    def parse(self, response):
         movies = response.xpath('//ol[@class=''row]/li')
         for each_movie in movies:
              item = MovieItem()
              item['name']=each_movie.xpath('article/h3/a/@title').extract()[0]
              yield item
