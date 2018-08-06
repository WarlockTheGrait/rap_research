# -*- coding: utf-8 -*-
# getting songs of found artists from www.last.fm
# needs results of searching albums
# example of artist page: https: https://www.last.fm/ru/music/Oxxxymiron/+tracks
# result: {"type": "songs_info", "album": album, "artist": arist, "songs": song} 
import json
import scrapy


class LastFMRapSpider_Songs(scrapy.Spider):
    name = 'rap_text_scrapping_songs'
    start_url = 'https://www.last.fm/ru/music'
    album_names = []

    def start_requests(self):
        file = open(self.settings['INIT_ALBUMS_INFO'], 'r')
        inform = json.loads(
            file.read())  # не самое лучшее решение. лпотом как-нибудь объясню почему - но лучше было бы читать по строке и yield
        file.close()  # и файлы закрывай, ЕПТ
        names_of_albums = []
        names = []
        names_of_artists = []
        for i in inform:
            for j in i["album"]:
                names_of_albums.append(j)
                names.append(i["name"])

        self.album_names = names_of_albums  #:)

        for i in names:
            names_of_artists.append(i[0])

        for counter in range(1, len(names_of_artists)):
            request = scrapy.Request(self.start_url + "/" + names_of_artists[counter] + "/" + names_of_albums[counter],
                                     callback=self.get_songs)
            request.meta['CONCRETE_ALBUM'] = names_of_albums[counter]
            request.meta['CONCRETE_ARTIST'] = names_of_artists[counter]
            yield request

    def get_songs(self, response):

        number_of_tracks = response.selector \
            .xpath("//*[@id='mantle_skin']/div[4]/div/div[1]/div[2]/div[1]/ul/li[2]/p/span/text()").extract()
        #print(number_of_tracks)
        songs = response.selector.xpath("//*[@id='tracks-section']/table/tbody/tr/td[4]/span/a/text()").extract()
        album = response.selector.xpath("//span[@class='header-title']/text()")
        #print(album)
        for (song) in zip(songs):
            yield {"type": "songs_info", "album": response.meta['CONCRETE_ALBUM'],
                   "artist": response.meta['CONCRETE_ARTIST'], "songs": song}
