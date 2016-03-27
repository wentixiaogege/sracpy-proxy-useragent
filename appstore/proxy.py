#!/usr/bin/python
#-*-coding:utf-8-*-

import random
import scrapy

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

class RandomProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, proxy_ip=''):
        self.proxy_ip = proxy_ip

    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        if ip:
            print ip
            request.meta['proxy']= ip

    #turns out only several ip works here
    proxy_list = [  "http://206.109.4.94:8080",
                    "http://202.103.215.199:80",
                    "http://171.35.242.139:80",
                    "http://52.76.170.159:80",
                    "http://54.183.234.224:8080",
                    "http://124.193.9.6:3128",
                    "http://54.183.214.25:8083",
                    "http://41.215.240.161:3128",
                    "http://221.211.117.140:3128",
                    "http://190.131.215.52:80"]
