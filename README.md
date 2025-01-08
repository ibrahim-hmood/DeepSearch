# DeepSearch
DeepSearch is a service that gathers adult content (both deep fake and not), and uses that to identify if any content being uploaded to it is deepfake or not. This is extremely beneficial in reducing the spread of adult deepfake content, which have real-world harm.

# Roadmap
Currently, my roadmap looks like this. It is very basic:
    [x] develop a basic web crawler
    [ ] develop a convolutional neural network for video processing
    [ ] develop a recurrent neural network for image processing

# How to test
To test this, run the following code:
```python
from crawler.crawler import Crawler
from config import DeepConfig

crawler = Crawler(DeepConfig("./adfconfig.conf"))
crawl_results = adf.crawl("[URL]")
crawler.save_videos(crawl_results, "test/videos")
```

Keep in mind that crawl_videos and crawl_images is not defined in Crawler. It is best to use a pre-defined web crawler, such as ADFCrawler.
You must still provide your own URL, should be obvious for which site.