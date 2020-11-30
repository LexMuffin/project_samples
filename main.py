import os
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from badoo_parse import settings
from badoo_parse.spiders.badoo import BadooSpider
from badoo_parse.spiders.aliexpress import AliexpressSpider

load_dotenv('.env')

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(AliexpressSpider)
    crawl_proc.start()

# if __name__ == '__main__':
#     crawl_settings = Settings()
#     crawl_settings.setmodule(settings)
#     crawl_proc = CrawlerProcess(settings=crawl_settings)
#     crawl_proc.crawl(BadooSpider, login=os.getenv('USER'), password=os.getenv('PASSWORD'))
#     crawl_proc.start()
