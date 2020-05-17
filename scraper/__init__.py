from .file_based_scrapper import FileScrapper
from .api_based_scrapper import APIScrapper

FILE_SCRAPER = 1
API_SCRAPER = 2

SCRAPPERS = {
    FILE_SCRAPER: FileScrapper,
    API_SCRAPER: APIScrapper
}


def get_scraper(*, scrapper_type: int, **kwargs):
    return SCRAPPERS[scrapper_type](**kwargs)
