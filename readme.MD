This is the python 2.7 version scrapy project,basic is write a python spider to get app infor from appstore.huawei.com website. Store it into a json format file .refre to https://www.youtube.com/watch?v=qVGU1Nx_jYA for more and basic understanding.

###using scrapy
Default structure of Scrapy projects
Before delving into the command-line tool and its sub-commands, let’s first understand the directory structure of a Scrapy project.

Though it can be modified, all Scrapy projects have the same file structure by default, similar to this:

scrapy.cfg
myproject/
    __init__.py
    items.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
The directory where the scrapy.cfg file resides is known as the project root directory. That file contains the name of the python module that defines the project settings. 

for more understanding http://scrapy.readthedocs.org/en/latest/topics/commands.html#topics-project-structure

###using splash
Splash is a lightweight headless browser that works as an HTTP API. Guess what, it's also Open Source. With Splash, you can easily render Javascript pages and then scrapy them!
There's a great and detailed tutorial about integrating Splash and ScrapyJs at Scrapinghub blog. After configuring everything, you can trigger the following requests:

def parse_locations(self, response):
    yield Request(url, callback=self.parse_response, meta={
                      'splash': {
                                  'endpoint': 'render.html',
                                  'args': {'wait': 0.5}
                      }
                })
Adding splash directive makes the script to call Splash, through render.html API and execute all Javascript of the crawled page.

###using user-agent
user-agent working like a tag of the browsers ,change it randomly can hide your info to the server:
two steps: 
         1. edit the settings.py 
         2. add random_useragent.py

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self,request,spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            print ua
            request.headers.setdefault('User-Agent', ua)

    #turns out only several ip works here
    user_agent_list = [......]


###using http-proxy
Working like the user-agent 
class RandomProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, proxy_ip=''):
        self.proxy_ip = proxy_ip

    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        if ip:
            print ip
            request.meta['proxy']= ip

    #turns out only several ip works here
    proxy_list = [  "http://206.109.4.94:8080",]

get the proxy your can refer to http://spys.ru/en/http-proxy-list/


##hide host for server

install docker + spash to handle with the js rendering service `:1

1.install docker
curl -fsSL https://get.docker.com/ | sh
2.make sure docker works
sudo docker run hello-world
3.install rendering servicer
sudo docker pull scrapinghub/splash
4.
sudo docker run -p 8050:8050 scrapinghub/splash
or???
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash

5.
install scrapyjs
 sudo pip install scrapyjs

splash now available at 0.0.0.0 at ports 8050

communications


request->splash service -> huawei app store
                              |
                           splash service 
                              | js rendering
                           response
                            
     
two ways for server block request ip
1. random proxy for user-agent
2. random proxy ip


##understanding deploy

here the deploy means that you can deploy your project and your spiders to the deamon server scrapyd ,just like you can deploy your website to the tomcat servers.

your can learn how to do this from :
https://scrapyd.readthedocs.org/en/latest/install.html

