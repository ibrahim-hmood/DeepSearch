from crawler.crawler import Crawler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#Crawler that crawls ADF
class ADFCrawler (Crawler):
    """
    crawl_videos: gets as many videos from a url as possible
    @param url: url which may contain videos
    @returns list of video links found
    """
    def crawl_videos(self, url: str):
        #Get all parameters
            #Should we stay in the domain or not
        stay_in_domain = self.config().get_bool("stay_in_domain")
            #What the maximum depth is
        max_depth = self.config().get_int("max_depth")
            #What our tags are
        url_tags = self.config().get_list("tags")
        #Find all videos
            #Connect to the new url
        if(self.depth() < max_depth):
            self.get(url)
            #And get all video elements
        video_elements = self.driver.find_elements(By.TAG_NAME, "video")
        if(len(video_elements) > 0):
            video_links = [video_element.get_attribute("src") for video_element in video_elements]
            return video_links
        else:
            #Try and crawl through this link
            if(self.depth() < max_depth):
                crawl_results = self.crawl(url)
                if(crawl_results is not None):
                    return crawl_results[0]
        
        #And navigate back
        self.driver.back()

    """
    crawl_images: gets as many images from a url as possible
    @param url: url which may contain images
    @returns nothing, as ADF does not have DF images
    """
    def crawl_images(self, url: str, stay_in_domain: bool = True, max_depth: int = 5, url_tags: list = None):
        #Get all parameters
            #Should we stay in the domain or not
        stay_in_domain = self.config().get_bool("stay_in_domain")
            #What the maximum depth is
        max_depth = self.config().get_int("max_depth")
            #What our tags are
        url_tags = self.config().get_list("tags")
        return [None]