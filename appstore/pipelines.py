# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class AppstorePipeline(object):
    def __init__(self):
        self.file = open('huaweiappstore.json','wb')
        #self.file1 = open('huaweiappstore.dat','wb')
   
    def process_item(self, item, spider):
        line = json.dumps(dict(item))+"\n"
        #val = "{0}\t{1}\t{2}\t{3}\t{4}\n".format(item['appid'],item['title'],item['intro'],item['thumbnail'],item['recommended'])
        #self.file1.write(val)
        self.file.write(line)
        return item
