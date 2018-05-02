from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from rap_scrapping.spiders import RapTextSpider_Songs


def run():
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result_songs.json')
    settings.set("FEED_EXPORT_ENCODING", 'utf-8')
    settings.set("INIT_ALBUMS_INFO", "result_albums.json")
    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(RapTextSpider_Songs.LastFMRapSpider_Songs)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished


if __name__ == '__main__':
    run()