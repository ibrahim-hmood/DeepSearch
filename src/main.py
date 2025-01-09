from config import DeepConfig
from crawler.adf import ADFCrawler
from crawler.crawler import Crawler
from os.path import dirname, realpath
from sys import argv


def show_help():
    #Print all of our options
    print("DeepSearch: identify if content is deepfake using REST API.")
    print("Usage: python3 src/main.py [URL] [OPTIONS]")
    print("Options and usages:")
    print("\tWeb Crawler:")
    print("\t\t--config PATH: runs with a different configuration path")
    print("\t\t--url URL: crawls a URL in this CLI method")
    print("\t\t--output_dir PATH: sets the output directory for saved images and videos")
    print("\tGeneral:")
    print("\t--help / --h: shows this help menu")

def main(args):
    #Check if enough arguments are passed
    if((len(args) < 1) or ("--help" in args) or ("--h" in args)):
        #Show the help menu
        show_help()
        #And leave
        exit()

    #Convert all arguments to lower case
    args = [arg.lower() for arg in args]

    #Now check if a configuration path is provided
    if("--config" in args):
        #Get the configuration path
        config_path = args[args.index("--config") + 1]
    else:
        #Use the default configuration file
        config_path = "{}/assets/adfconfig.conf".format(dirname(realpath(__file__)))
    
    #Check if the URL is set
    if(len(args) > 1):
        #Get the passed URL
        url = args[1]

    if("--url" in args):
        #Get the crawler url
        url = args[args.index("--url") + 1]
    
    #Now get the configuration data
    config = DeepConfig(config_path)
    
    #Check if the output directory is set
    if("--output_dir" in args):
        #Get the output directory
        output_dir = args[args.index("--output_dir") + 1]
    else:
        #Use the default output directory
        output_dir = "{}/crawler/{}/".format(dirname(dirname(realpath(__file__))), config.get("label"))

    #Now get the type of crawler
    if(ADFCrawler.__name__ in config.get("crawler")):
        crawler = ADFCrawler(config)
    
    #And crawl the given URL
    crawl_results = crawler.crawl(url)

    #Now save the videos
    crawler.save_videos(crawl_results, output_dir)
if(__name__ == "__main__"):
    main(argv)