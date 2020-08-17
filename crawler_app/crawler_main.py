
from crawler_core import CrawlerCore
import sys

class CrawlerMain:

    def __init__(self, uri,recursive = True):
        self.crawler_execute = CrawlerCore()
        self.uri = uri
        self.recursive_fetch = recursive
        self.log = self.crawler_execute.log
    
    def start_crawler(self, ):
        try:
            list_of_links = self.crawler_execute.crawler_run(self.uri)
            if list_of_links:
                self.log.info("************Successfully Ran the Crawler**********")
                for link, pages in list_of_links.items():
                    self.log.info("******  For URL  ******: %s",link)
                    for each in pages:
                        self.log.info("              LINK     : %s",each)
                        
                        
            else:
                self.log.error("Error in Crawler Execution, pls check the logs")
                print ("Error in Crawler Execution, pls check the logs")
        except Exception as e:
            self.log.error("Error in Crawler Execution %s", e)
            print ("Error in Crawler Execution, pls check the logs")
    
    


if __name__ == "__main__":
    if len(sys.argv)>1:
        uri =  sys.argv[1]
        if any(ext in uri for ext in ("https://","http://")):
            trigger = CrawlerMain(uri)
            trigger.start_crawler()
        else:
            print ("Please give a valid URL")
    else:
        print ("Please provide parameters")
    

