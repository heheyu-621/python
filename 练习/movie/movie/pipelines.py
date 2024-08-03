# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
class MoviePipeline(object):
    def open_spider(self,spider):
        self.file = open('log.txt', 'w', encoding='utf-8')
    def close_spider(self,spider):
        self.file.close()
    def process_item(self,item,spider):
         self.file.write(str(item)+'\n')