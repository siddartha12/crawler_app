

import requests
from parsel import Selector
from utilities import LogManager
from crawler_init import CrawlerInit
import time
from requests.exceptions import Timeout, RequestException
start = time.time()

class CrawlerCore:
    
    def __init__(self):
        self.all_links = {}
        self.log= LogManager().get_logger()
        self.config = CrawlerInit()
        self.crawl_response = None
        self.method= 'GET'
        self.links = None
        self.inner_links = None
        
    def call_api(self,uri, method):
        bad_request_flag = False
        if uri:
            response = None
            self._retried = 0
            try:
                if method == 'GET':
                    response = requests.get(uri, verify=False, timeout=self.config.time_out)
                else:
                    self.log("Not supporting other methods")
    
                if response is not None:
                    if response.status_code == 401: # Unauthorized
                        self.log.info("Not authorized")
                        return False
                    elif response.status_code == 429 or response.status_code == 500 or (response.status_code==400 and str(response.text).__contains__("Wrong Session ID")): #Attempt retry for internal server error and too many requests
                        if response.status_code == 400:
                            bad_request_flag = True
                        if bad_request_flag:
                            self.log.error("Internal Errors")
                            return False
                        else:
                            self.Log.error("Internal server error")
                            return False
                    elif response.status_code == 400 and not bad_request_flag:#Bad request
                        self.log.error("Bad Request")
                        raise Exception(response.text)
                    elif response.status_code in (200, 201, 202):
                        return response
                    elif response.status_code == 503:
                        raise Exception("503 service unavailable")
                    else:
                        self.log.warn("Unknown error Occurred")
                        raise Exception(response.text)
                else:
                    self.log.error("No response")
                    raise Exception("No response from the server")
            except requests.exceptions.Timeout as ti:
                self.log.error("Time out")
                raise Exception(response.text)

            except RequestException as re:
                self.log.warn("Current Request has been closed.")
                return False
            except Exception as e:
                self.log.warn("Un-handled Exception")
                return False
    
    

    def crawler_run(self, URI):
        try :
            self.crawl_response = self.call_api(URI,self.method)
            selector = Selector(self.crawl_response.text)
            #Parse all the links
            self.links = selector.xpath('//a/@href').getall()
            self.log.info("Crawling in Progress........ ")
            self.log.info(self.links)
            counter = 0
            for each in self.links:
                self.log.info("LINK     : %s ",each)
                counter += 1
            self.log.info("Crawling Completed........ ")
            self.log.info("Total links retrieved from page: %s ",counter)
            for link in self.links:
                try:
                    response = self.call_api(link, self.method)
                    if response :
                        selector = Selector(response.text)
                        if response.status_code == 200:
                            self.inner_links = selector.xpath('//a/@href').getall()
                            self.all_links[link] = self.inner_links
                    else:
                        self.log.debug("Getting response in progress...")
                except UnicodeEncodeError as exp:
                    self.log.error("Uni-code Error %s", exp)
                except KeyError as exp:
                    self.log.error("Key Error %s", exp)
                except Exception as exp:
                    self.log.error(exp)     
            return self.all_links
        #To Do: we need to add specific  exceptions
        except Exception as e:
            self.Log.error("Error in Crawler parse %s", e)
            return self.all_links
    

