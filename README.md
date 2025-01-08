# DeepSearch
DeepSearch is a service that gathers adult content (both deep fake and not), and uses that to identify if any content being uploaded to it is deepfake or not. This is extremely beneficial in reducing the spread of adult deepfake content, which have real-world harm.

# Roadmap
Currently, my roadmap looks like this. It is very basic:
- [x] create a basic web crawler
- [x] create a web crawler for deep fake content
- [ ] create a web crawler for non-deepfake content
- [ ] create a convolutional neural network for video classification
- [ ] create a recurrent neural network for image classification
- [ ] start training the neural networks
- [ ] test and re-train until networks are above 90% accurate
- [ ] host this service using REST API and Flutter

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