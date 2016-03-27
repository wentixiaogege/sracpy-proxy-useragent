#!/usr/bin/env python2.7
# -*- coding utf-8 -*-


import scrapy
import re
from scrapy import Selector
from appstore.items import AppstoreItem

class HuaweiAppSpider(scrapy.Spider):
    name = "huawei"
    allowed_domains = ["appstore.huawei.com"]
    start_urls = [
        "http://appstore.huawei.com/more/all/1",
    ]

    script = """
        function main(splash)
            splash:autoload("https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js")
            splash:go("http://example.com")
            splash:runjs("$('#some-button').click()")
            return splash:html()
        end
        """
    def parse(self, response):
        hrefs = response.selector.xpath('.//h4[@class="title"]/a/@href')

        for href in hrefs:
            yield scrapy.Request(href.extract(),callback = self.parse_recommended,meta={
             'splash': {
                     'endpoint': 'render.html',
                     'args': {'wait': 0.5,
                              }
                 }
                 })
        
        # yield scrapy.Request(response.url,self.parse,meta={
        #     'splash': {
        #             'endpoint': 'execute',
        #             'args': {'lua_source': script,
        #                      }
        #         }
        #         })
    def find_next_page(self,url):
        try:
            page_num_str = url.split('/')[-1]
            page_num = int(page_num_str) +1;
            url = url[:-len(page_num_str)] + str(page_num)
            return url
        except ValueError:
            print "### page cannot be handled"
            print url
            return "http://google.com"
    def parse_recommended(self,respone):
        item = AppstoreItem();

        page = Selector(respone)

        item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
        item['url'] = respone.url
        appid = re.match(r'http://.*/(.*)',item['url']).group(1)
        item['appid'] = appid
        #item['intro'] = page.xpath('//div[@class="content"]/div[@id="app_strdesc"]/text()').extract_first().encode('utf-8')
        #item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
        item['thumbnail'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first();
        divs = page.xpath('//div[@class="open-info"]')

        recommens = ""
        for div in divs:
            url = div.xpath('./p[@class="name"]/a/@href').extract_first().encode('utf-8')
            recommenAppId = re.match(r'http://.*/(.*)',url).group(1)
            recommenTitle = div.xpath('./p[@class="name"]/a/@title').extract_first().encode('utf-8')
            recommens += "{0}:{1},".format(recommenAppId,recommenTitle)

        #item['recommended'] = recommens

        yield item