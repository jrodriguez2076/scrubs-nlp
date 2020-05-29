# -*- coding: utf-8 -*-
import scrapy
import json
import os

class ScriptContentSpider(scrapy.Spider):
    name = 'content'
    counter = 0
    season = 0

    def __init__(self, *args, **kwargs):
        self.season = kwargs.get('season')

    def start_requests(self):
        urls = []
        with open ('script_urls_' + str(self.season) + '.json') as links:
            content = json.load(links)
            urls = content['urls']
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        script = response.css('div.mw-content-text')
        texts = script.css('p,h2::text').getall()
        self.counter += 1
        filename = 'S0'+ str(self.season) + '-E' + str(self.counter) + '.txt'
        print('***************')
        print(os.path.join(os.getcwd(),'scripts', filename))
        with open(os.path.join(os.getcwd(),'scripts', filename), "w") as f:
            for text in texts:
                f.write(text)
        pass
