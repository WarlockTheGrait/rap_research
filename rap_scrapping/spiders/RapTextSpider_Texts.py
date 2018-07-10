import json

import scrapy


class GeniusRapSpiderSongs(scrapy.Spider):
    name = 'rap_text_scrapping_songs'
    start_url = 'https://genius.com'

    def start_requests(self):
        file = open(self.settings['INIT_SONGS_INFO'], 'r')
        inform = json.loads(
            file.read())
        file.close()
        names_of_artists = []
        names_of_songs = []
        for i in inform:
            names_of_artists.append(i["artist"])
            names_of_songs.append(i["song"])
        for counter in range(1, len(names_of_artists)):
            request = scrapy.Request(self.start_url + "/search?q=" + names_of_artists[counter].replace(" ", "%20") +
                                     '+' + names_of_songs[counter].replace(" ", "%20"),
                                     callback=self.song_page)

            yield request

    def song_page(self, response):

        # getting link of page of song. Nothing works here :( Only one variant of xpath works :
        # //div/div/div/a/@href

        link = response.selector.xpath("/html/body/routable-page/ng-outlet/search-results-page/div/div[1]/h2/text()")\
            .extract()
        answer = scrapy.Request(link,
                                callback=self.get_text)
        return answer

    def get_text(self, response):

        # this xpath also awful. I don't have opportunity to check validity of this shit.

        name = response.selector.xpath(
            '/html/body/routable-page/ng-outlet/song-page/div/div/header-with-cover-art/div/div/div[1]/div['
            '2]/div/ng-transclude/metadata/h3[2]/expandable-list/div/span[2]/span/a/text()').extract()
        album = response.selector.xpath("/html/body/routable-page/ng-outlet/song-page/div/div/header-with-cover-art"
                                        "/div/div/div[1]/div[2]/div/ng-transclude/metadata/h3["
                                        "3]/song-primary-album/div/span[2]/a/text()").extract()
        text = response.selector.xpath(
            '/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile['
            '1]/lyrics/div/section/p/text()').extract()

        for name in zip(name):
            yield {"type": "song_info", "name": name, "album": album, "text": text}
