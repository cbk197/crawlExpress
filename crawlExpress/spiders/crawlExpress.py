import scrapy 
import json 
import os
import os.path
from crawlExpress.items import CrawlexpressItem
class CrawlExpress(scrapy.Spider):
    name = "express"
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = []
        links = response.xpath("//*[@id=\"main_menu\"]/a") 
        for l in links : 
            tmp = l.xpath("@href").extract_first()
            if "https://vnexpress.net" not in l.xpath("@href").extract_first():
                tmp = "https://vnexpress.net"+ tmp 
            urls.append(tmp)
        urls = urls[3:]
        for url in urls:
            yield scrapy.Request(url = url,callback = self.parseTopic)
    
    def parseTopic(self, response):
        urls = []
        links = response.css('html body section.container section.sidebar_1 article.list_news h4.title_news a')
        for l in links : 
            urls.append(l.xpath("@href").extract_first())
        for url in urls :
            yield scrapy.Request(url = url,callback = self.parseContent)
        
        
    def parseContent(self, response):
        topic = u""
        topiclink = response.xpath('/html/body/section[1]/ul/li/h4/a')
        item = CrawlexpressItem()
        if topiclink != [] :
            topic = topiclink[0].xpath("text()").extract_first()
            PathDir = u"crawlExpress\data\\" + topic.replace(' ', '_')
            
            if  not os.path.exists(PathDir) :
                os.mkdir(PathDir)
            filename1 = u""
            if topic == u"Sức khỏe" :
                filename1 = response.xpath('/html/body/section[2]/section[1]/h1').xpath("text()").extract_first()
                filename = filename1.replace(' ', '_')
                filename = filename.replace('|', '_')
                filename = filename.replace('*', '_')
                filename = filename.replace('\\', '_')
                filename = filename.replace('?', '_')
                filename = filename.replace(':', '_')
                filename = filename.replace('\"', '_')
                filename = filename.replace('\n', '_')
                filename = filename.replace('\t', '_')
                pathfile = PathDir + "\\" + filename + '.json'
                item['Link'] = response.url
                item['Title'] = filename1
                content = u""
                content = content + response.xpath('/html/body/section[2]/section[1]/p').xpath("text()").extract_first()
                ptags = response.xpath('/html/body/section[2]/section[1]/article/p')
                for ptag in ptags :
                    if isinstance( ptag.xpath("text()").extract_first(),str):
                        content = content + " " + ptag.xpath("text()").extract_first()
                item['Content'] = content
                if not os.path.exists(pathfile) :
                    f = open(pathfile,'w',encoding='utf-8')
                    json.dump(dict(item),f,ensure_ascii= False)
                    f.close()
            else:
                filename1 = response.xpath('/html/body/section[2]/section[1]/section[1]/h1').xpath("text()").extract_first()
                filename = filename1.replace(' ', '_')
                filename = filename.replace('|', '_')
                filename = filename.replace('*', '_')
                filename = filename.replace('\\', '_')
                filename = filename.replace('?', '_')
                filename = filename.replace(':', '_')
                filename = filename.replace('\"', '_')
                filename = filename.replace('\n', '_')
                filename = filename.replace('\t', '_')
                pathfile = PathDir + "\\" + filename +'.json'
                item['Link'] = response.url
                item['Title'] = filename1
                content = u""
                content = content + response.xpath('/html/body/section[2]/section[1]/section[1]/p').xpath("text()").extract_first()
                # print("========================================",response.xpath('/html/body/section[2]/section[1]/section[1]/p').xpath("text()").extract_first())
                ptags = response.xpath('/html/body/section[2]/section[1]/section[1]/article/p')
                for ptag in ptags :
                    if isinstance( ptag.xpath("text()").extract_first(),str):
                        content = content + " " + ptag.xpath("text()").extract_first()
                item['Content'] = content
                if not os.path.exists(pathfile) :
                    f = open(pathfile,'w',encoding='utf-8')
                    json.dump(dict(item),f,ensure_ascii= False)
                    f.close()



            
            