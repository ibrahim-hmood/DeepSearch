from crawler.adf import ADFCrawler
from config import DeepConfig

def main():
    adf = ADFCrawler(DeepConfig("adfconfig.conf"))
    crawl_res = adf.crawl("https://adultdeepfakes.com/")
    adf.save_videos(crawl_res, "test/videos")

if(__name__ == "__main__"):
    main()