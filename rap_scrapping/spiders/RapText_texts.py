import scrapy
import json
# gets texts of songs from rap-text.ru
# result: artist_name__song_name.json
# {"artist": ***, "title": ***, "text": ***}


class RapTextSpider(scrapy.Spider):
    name = 'genius_texts'
    start_url = 'http://rap-text.ru'

    def start_requests(self):
        return [scrapy.Request(self.start_url, callback=self.get_alphabet_pages)]

    def get_alphabet_pages(self, response):
        raw_pages_lat = response.selector.xpath("/html/body/div/div[1]/nav/div/ul[1]/li/a/@href").extract()
        raw_pages_ru = response.selector.xpath("/html/body/div/div[1]/nav/div/ul[2]/li/a/@href").extract()
        raw_pages = raw_pages_lat + raw_pages_ru
        print("raw_pages")
        print(raw_pages)

        answer = [scrapy.Request(i, callback=self.get_artists_page) for i in
                  raw_pages]
        return answer

    def get_artists_page(self, response):
        pages_of_artists = response.selector.xpath("//*[@id='dle-content']/div[2]/div[1]/li/a/@href").extract()

        answer = [scrapy.Request(i, callback=self.parse_artist_page) for i in
                  pages_of_artists]
        print("pages_of_songs")
        print(response.url)
        print(pages_of_artists)
        return answer

    def parse_artist_page(self, response):
        pages_of_songs = response.selector.xpath("//*[@id='dle-content']/div[2]/div[1]/li/a/@href").extract()

        answer = [scrapy.Request(i, callback=self.parse_song_page) for i in
                  pages_of_songs]
        return answer

    def parse_song_page(self, response):
        id = response.url.split('/')[4].split('-')[0]  # костыль из-за струтуры сайта
        xpath = '//*[@id="news-id-' + id + '"]'  # //*[@id="news-id-****"]
        text = response.selector.xpath(xpath + "/text()").extract()
        name_of_artist = response.selector.xpath(xpath + "/span/text()").extract()[0].split(" - ")[0]
        name_of_song = response.selector.xpath(xpath + "/span/text()").extract()[0].split(" - ")[1].\
            split(" (текст песни)")[0]

        dict = {"artist": name_of_artist, "title": name_of_song, "text": text}

        artist = name_of_artist.replace(" ", "_")
        song = name_of_song.replace(" ", "_")
        filename = artist + "__" + song + ".json"

        f = open(filename, "w")
        json.dump(dict, f, ensure_ascii=False)
        f.close()
