# -*- coding: utf-8 -*-
import scrapy


class LastFMRapSpiderNew(scrapy.Spider):
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

        for link in links:
            yield scrapy.Request(link + "/+albums", callback=self.get_albums)

        #for (name, link) in zip(names, links):
            #yield {"type": "artist_info", "name": name, "link": link}

    def get_albums(self, response):
        #parsing album page of artist
        raw_pages = response.selector.xpath("//*[@id='artist-albums-section']/nav/ul/li/a/@href").extract()
        pages = [int(data.replace("?page=", "")) for data in raw_pages]
        if not pages:
            answer = [scrapy.Request(response.request.url, callback=self.parse_album_page)]
        else:
            max_page = max(pages)
            answer = [scrapy.Request(response.request.url + "?page=" + str(i), callback=self.parse_album_page) for i in
                  range(1, max_page + 1)]

        return answer

    def parse_album_page(self, response):
        #list of albums for every page

        albums = response.selector.xpath("//h3[@class='album-grid-item-title']/a/text()").extract()
        name = response.selector.xpath("//h1[@class='header-title']/a/text()").extract()

        for (name) in zip(name):
            yield {"type": "artist_info", "name": name, "album": albums}
