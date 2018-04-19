# -*- coding: utf-8 -*-
import scrapy


class LastFMRapSpider(scrapy.Spider):
    name = 'rap_text_scraping'
    start_url = 'https://www.last.fm/ru/tag/russian+rap/artists'

    def start_requests(self):
        return [scrapy.Request(self.start_url, callback=self.get_pages)]

    def get_pages(self, response):
        raw_pages = response.selector.xpath("//div[4]/div/div[1]/nav/ul/li/a/@href").extract()
        pages = [int(data.replace("?page=", "")) for data in raw_pages]
        max_page = max(pages)

        answer = [scrapy.Request(self.start_url + "?page=" + str(i), callback=self.parse_artists_page) for i in
                  range(1, max_page + 1)]
        return answer

    def parse_artists_page(self, response):
        # links for artists pages
        links = response.selector.xpath("//h3[@class='big-artist-list-title']/a/@href").extract()
        links = [response.urljoin(link) for link in links]

        # artists names
        names = response.selector.xpath("//h3[@class='big-artist-list-title']/a/text()").extract()

        # num listeners of artist, will use it Farther to filter data
        num_listeners = response.selector.xpath("//p[@class='big-artist-list-listeners']/text()").extract()
        num_listeners = [int(listeners.strip().replace(u'\xa0', "")) for listeners in num_listeners if
                         len(listeners.strip()) > 0]

#        for link in links:
#            yield scrapy.Request(link, callback=self.parse_concrete_artist_page)

        for (name, link, num_listeners_concrete) in zip(names, links, num_listeners):
            yield {"type": "artist_info", "name": name, "link": link, "listeners": num_listeners_concrete}

    # find https://www.last.fm/ru/music/Guf/+tracks tracks here
    # find albums titles and years here https://www.last.fm/ru/music/Guf/+albums?page=2
    # store in json too
    def parse_concrete_artist_page(self, response):

        print("HAHAHA")
