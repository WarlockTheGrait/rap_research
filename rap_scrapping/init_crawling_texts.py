from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from rap_scrapping.genius_spiders import texts_of_songs


def run():
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result_songs_texts.json')
    settings.set("FEED_EXPORT_ENCODING", 'utf-8')
    settings.set("INIT_SONGS_INFO", "result_songs.json")
    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(texts_of_songs.GeniusRapSpiderSongs)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished


if __name__ == '__main__':
    run()
