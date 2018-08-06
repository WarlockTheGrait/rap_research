from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from rap_scrapping.spiders import LastFM__artist_info
from rap_scrapping.spiders import LastFM__albums
from rap_scrapping.spiders import LastFM__songs


def run_artist_info():
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result.json')
    settings.set("FEED_EXPORT_ENCODING", 'utf-8')
    settings.set("CONCURRENT_REQUESTS ", 32)
    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(RapTextSpider.LastFMRapSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished
    
    run_albums()
    

def run_albums():
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result_albums.json')
    settings.set("FEED_EXPORT_ENCODING", 'utf-8')
    settings.set("INIT_ARTISTS_INFO", "result.json")
    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(RapTextSpider_Albums.LastFMRapSpider_Albums)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run() # the script will block here until all crawling jobs are finished
    
    run_songs()

    
def run_songs():
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
