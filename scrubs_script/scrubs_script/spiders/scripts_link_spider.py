import scrapy
import json

class ScriptSpider(scrapy.Spider):
    name = "script"
    full_links = []
    episodes_names = []
    season = 0

    def __init__(self, *args, **kwargs):
        self.season = kwargs.get('season')

    def start_requests(self):
        urls = ['https://scrubs.fandom.com/wiki/Category:Season_' + str(self.season) + '_Transcripts']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        links = response.css('a')
        domain = 'https://scrubs.fandom.com'
        transcripts = response.xpath("//p/a[contains(text(),'transcript')]")
        for transcript in transcripts:
            transcript_link = transcript.css('a::attr(href)').get()
            try:
                self.full_links.append(domain + transcript_link)
                self.episodes_names.append(transcript_link[len('/wiki/'):transcript_link.find('_transcript')])
            except:
                pass
        links_urls = {
                "urls": self.full_links
            }
        links_urls_parsed = json.dumps(links_urls)
        with open('script_urls_' + str(self.season) + '.json', 'w') as f:
            f.write(links_urls_parsed)

        episodes_names = {
            "names": self.episodes_names
        }
        episodes_names_parsed = json.dumps(episodes_names)
        with open('episodes_' + str(self.season) + '.json', 'w') as f:
            f.write(episodes_names_parsed)
        

