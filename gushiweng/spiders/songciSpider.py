#-*- coding:utf-8 -*-

'''
    -----------------------------------------------------------------------------
    Create:
    ----------------------------------------------------------------------------- 
        |Description: 爬取古诗文网宋词300首，保存为csv文件
        |Author: huangwei
        |Date: 2016-5-19
        |Version: 1.0
    -----------------------------------------------------------------------------
    Change Log:
    -----------------------------------------------------------------------------
        |Description: scrapy crawl songci
        |Author: 
        |Date: 
        |Version: 
    -----------------------------------------------------------------------------

'''

import scrapy
from gushiweng.items import songciIndexItem, songciPoemItem
from lxml import html
import HTMLParser
import re
import json
import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

filename = 'poem.csv'

class songciSpider(scrapy.Spider):
    name = 'songci'
    #allowed_domains = ['']
    start_urls = [
        'http://so.gushiwen.org/gushi/songsan.aspx',
    ]
    
    def __init__(self):        
        self.fpoem = open(filename, 'wb')
        self.fpoem.write(codecs.BOM_UTF8)
        self.poemcsv = csv.writer(self.fpoem, dialect='excel')        
        self.poemcsv.writerow([u'标题',u'评分',u'朝代',u'作者',u'诗词内容',u'译文',u'赏析',u'作者简介'])
    
    def parse(self, response):        
        page = response.body
        filename = 'songciIndex.html'
        with open(filename, 'wb') as fp:
            fp.write(page)
        
        for url in self.indexPageParse(page):
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.poemPageParse)
                
    def indexPageParse(self, page):
        print "\t------Now Parse IndexPage------"
        response = html.fromstring(unicode(page, 'utf-8'))
        aSets = HTMLParser.HTMLParser().unescape(response.xpath('//div[@class="main3"]//span[descendant::a[contains(@href, "view")]]'))
        
        urls = []
        f = open('songci.txt','wb')
        for i in aSets:
            item = songciIndexItem()            
            item['href'] = 'http://so.gushiwen.org' + i.xpath('./a[@target="_blank"]/@href')[0]
            item['title'] = i.xpath('./a[@target="_blank"]/text()')[0].encode('utf-8','ignore')
            try:
                item['author'] = i.xpath('./text()')[0].encode('utf-8','ignore')
            except:
                item['author'] = 'none'
            #item['id'] = i
            
            print 'title : ',item['title'].decode('utf-8')
            f.write('title : %s\n' % item['title'])
            f.write('author : %s\n' % item['author'])
            f.write('href : %s\n' % item['href'])            
            urls.append(item['href'])
        f.close()
        return urls
        
    def poemPageParse(self, response):
        item = songciPoemItem()
        item['title'] = response.xpath('//h1/text()')[0].extract()
        item['score'] = response.xpath('//div[@class="line1"]/span/text()')[0].extract()
        item['dynasty'] = response.xpath('//div[@class="son2"]/p[1]/text()')[0].extract()
        try:
            item['author'] = response.xpath('//div[@class="son2"]/p[2]/a/text()')[0].extract()
        except:
            item['author'] = ''
        poems = ''
        for each in response.xpath('//div[@class="son2"]/text()').extract():
            poems += each
        item['poem'] = poems.strip()
        if item['poem'] == '':
            try:
                for each in response.xpath('//div[@class="son2"]/p[4]/text()').extract():
                    item['poem'] += each
                item['poem'] = item['poem'].strip()
            except:
                item['poem'] = 'Not found'
        try:
            item['translate'] = response.xpath('//div[contains(@id,"fanyiShort")]/p[2]/text()')[0].extract()
        except:
            item['translate'] = ''
        try:
            item['appreciate'] = response.xpath('//div[contains(@id,"shangxiShort")]/p[2]/text()')[0].extract()
        except:
            item['appreciate'] = ''
        authorInfo = ''
        for each in response.xpath('//div[@style="overflow:auto;"]/text()').extract():
            authorInfo += each        
        item['authorInfo'] = authorInfo.strip() 
        
        self.poemcsv.writerow([item['title'],item['score'],item['dynasty'],item['author'],item['poem'],item['translate'],item['appreciate'],item['authorInfo']])

        