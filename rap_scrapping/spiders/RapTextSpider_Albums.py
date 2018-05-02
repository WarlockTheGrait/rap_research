# -*- coding: utf-8 -*-
import json

import scrapy


class LastFMRapSpider_Albums(scrapy.Spider):
    name = 'rap_text_scraping_albums'

    def start_requests(self):
        filepath = self.settings['INIT_ARTISTS_INFO']
        file = open(filepath, 'r')
        inform = json.loads(file.read())
        links = []
        for i in inform:
            links.append(i["link"])
        file.close()  # ФАЙЛЫ ЗАКРЫВАЙ
        return [scrapy.Request(link + "/+albums", callback=self.get_albums) for link in
                links]

    def get_albums(self, response):
        # parsing album page of artist
        raw_pages = response.selector.xpath("//*[@id='artist-albums-section']/nav/ul/li/a/@href").extract()
        pages = [int(data.replace("?page=", "")) for data in raw_pages]
        if len(pages) == 0:
            answer = [scrapy.Request(response.request.url, callback=self.parse_album_page)]
        else:
            max_page = max(pages)
            answer = [scrapy.Request(response.request.url + "?page=" + str(i), callback=self.parse_album_page) for i in
                      range(1, max_page + 1)]

        return answer

    def parse_album_page(self, response):
        # list of albums for every page
        ##//*[@id='artist-albums-section']/nav/ul/li/a/@href
        ###########//h3[@class='album-grid-item-title']/a/text()
        # //*[@id="artist-albums-section"]/ol/li[1]/div/h3/a

        albums = response.selector.xpath("//h3[@class='album-grid-item-title']/a/text()").extract()
        name = response.selector.xpath("//h1[@class='header-title']/a/text()").extract()

        for (album) in zip(albums):
            yield {"type": "album_info", "name": name, "album": album}
