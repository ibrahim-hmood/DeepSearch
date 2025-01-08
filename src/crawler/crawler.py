from config import DeepConfig

from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from os.path import exists, isdir
from os import makedirs

import requests
from hashlib import sha512

import re
class Crawler:
    def __init__(self, config: DeepConfig):
        #Initialize variables
        #Create a chrome web driver
        self.__options = Options();
        self.__options.add_argument("--headless=new")
        self.__config = config
        self.driver = webdriver.Chrome(options = self.__options)
        self.visited = []
    

    """
    get: connects to a URL if one is given, returns current url otherwise
    @optional param url: optional url to connect to
    @returns current url
    """
    def get(self, url: str = None):
        #Make sure url is set
        if(url is not None):
            self.visited.append(url)
            self.driver.get(url)
        #And return current url
        return self.driver.current_url

    """
    get_domain: gets domain name of url
    @param url: url whose domain we want
    @returns domain name
    """
    def get_domain(self, url: str):
        regex = r"^(?:https?://)?(?:www\.)?([^\/]+)"
        match = re.match(regex, url)
        if(match):
            return match.group(1)
        return None
    
    """
    url_has_tags: checks if a url has any of the given tags in a list
    @param tags: tags to be checked
    @param url: url being tested
    """
    def url_has_tags(self, tags: list, url: str):
        #Check if any of the tags is in the URL
            #Go through all tags
        for tag in tags:
            #Check if current tag is in the URL
            if(tag in url):
                #It is, return true
                return True
            
        #No tag is in the url
        return False

    """
    crawl: gets all image and video urls in a given website
    @param url: url to be searched
    """
    def crawl(self, url: str):
        stay_in_domain = self.__config.get_bool("stay_in_domain")
        max_depth = self.__config.get_int("max_depth")
        url_tags = self.__config.get_list("tags")
        #Make sure we have not crawled this url
        if(url not in self.visited and self.depth() < max_depth):
            #Crawl url for as many videos and images as possibles
            videos = []
            images = []
                #Open the url for crawling
            self.get(url)
                #Get all links in the web page
            link_elements = self.driver.find_elements(By.TAG_NAME, "a")
            links = [link_element.get_attribute("href") for link_element in link_elements]
                #And crawl through them
            for link in links:
                if(link is not None and (link != url)):
                    #Get the domain for url
                    url_domain = self.get_domain(url)

                    #And the link's domain
                    link_domain = self.get_domain(link)

                    #Crawl under two conditions:
                        # (1) we should just crawl, not staying on the url's domain
                        # (2) we should stay on the url's domain, and it's and the link's domain are the same
                    if((not stay_in_domain) or (stay_in_domain and (url_domain == link_domain))):
                        #Check if we have any tags
                        if(url_tags is not None):
                            #Check if our url has any of the tags
                            if(self.url_has_tags(url_tags, link)):
                                #Get all videos on the link
                                video_crawl_results = self.crawl_videos(link)
                                if(type(video_crawl_results) is list):
                                    videos += video_crawl_results
                                else:
                                    videos.append(self.crawl_videos(link))

                                #And get all images
                                images.append(self.crawl_images(link))
                        else:
                            #Get all videos on the link
                            videos.append(self.crawl_videos(link))

                            #And get all images
                            images.append(self.crawl_images(link))
            #And return the videos and images links
            crawl_results = dict()
            crawl_results["videos"] = self.__fix_list(videos)
            crawl_results["images"] = images
            return crawl_results
    
    """
    __fix_list: removes none from list
    @param to_fix: list to be fixed
    @returns fixed list
    """
    def __fix_list(self, to_fix: list):
        fixed_list = list()
        for item in to_fix:
            if(type(item) is list):
                fixed_list += self.__fix_list(item)
            if(item is not None):
                fixed_list.append(item)
        return fixed_list

    """
    crawl_videos: gets as many videos from a url as possible
    @param url: url which may contain videos
    @returns list of video links found
    """
    def crawl_videos(self, url: str):
        pass

    """
    crawl_images: gets as many images from a url as possible
    @param url: url which may contain images
    @returns list of image links found
    """
    def crawl_images(self, url: str):
        pass

    """
    depth: returns numer of visited pages
    @returns amount of visited pages
    """
    def depth(self):
        #Just return the length of visited pages
        return len(self.visited)
    
    """
    config: gets current configuration
    @returns current configuration
    """
    def config(self):
        return self.__config
    
    """
    debugger: gets debugger in configuration
    @returns debugger
    """
    def debugger(self):
        return self.__config.debugger()

    """
    __gen_rand: generates a random string of variable length
    @param length: length of generated string
    @returns random string
    """
    def __gen_rand(self, length: int = -1):
        #Generate a random string containing both cases, numbers, and some symbols
        alphanumerosym = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789)!@#$%^&*(_+{][}';:/.>,<"
        if(length < 0):
            length = len(alphanumerosym)
        random_string = ""
        for index in range(length):
            random_string += alphanumerosym[randint(index, length)]
        
        #Return the generated string
        return random_string


    """
    save_videos: saves videos to a given folder
    @param crawl_results: results gathered from crawling
    @param save_path: where to save the videos
    """
    def save_videos(self, crawl_results: dict,  save_path: str):
        #Add the current crawler's name to the save path
        crawler_name = type(self).__name__
        if(crawler_name not in save_path):
            #Add the crawler name
            save_path += "/{}".format(crawler_name)
        
        #Create the save path
        if(not exists(save_path)):
            makedirs(save_path)
        
        #And save all the videos
            #Go through all video links
        video_links = crawl_results["videos"]
        for video_link in video_links:
            #Read the website's content
            content = requests.get(video_link, stream = True)
            content.raise_for_status()
            
            #Create a video file name
            save_name = "{}/{}.mp4".format(save_path, self.__gen_rand(self.__config.get_int("file_name_length")))

            #And save the video
                #Open the video save for writing
            with open(save_name, "wb") as video_file:
                #We started saving this video
                self.debugger().debug("Saving '{}' to '{}'...".format(video_link, save_name))
                #Go through all chunks in our content
                for chunk in content.iter_content(chunk_size = 8192):
                    #Write current chunk
                    video_file.write(chunk)