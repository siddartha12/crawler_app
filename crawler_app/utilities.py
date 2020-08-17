

from logging import Logger, StreamHandler, FileHandler, Formatter, Filter
import datetime
import os
from crawler_init import CrawlerInit




class LogManager(Logger, object):
    INSTANCE = None
    logFilePath = None
    UniqueId = None

    def __init__(self):
        self.config = CrawlerInit()
        self.time_now = datetime.datetime.now()
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists! Use get_instance method")
        Logger.__init__(self, "Crawler", 0)
        self.INSTANCE = self
        formatter = Formatter(self.config.log_formatter)
        dirname = self.config.dirname
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        file_handler = FileHandler(dirname + "/" + self.time_now.strftime("%Y%m%d-%H-%M-%S") + ".log")
        LogManager.logFilePath = file_handler.baseFilename
        stream_handler = StreamHandler()
        stream_handler.addFilter(FileExtensionFilter())
        file_handler.setFormatter(formatter)
        self.INSTANCE.addHandler(file_handler)
        self.INSTANCE.addHandler(stream_handler)

    @classmethod
    def get_logger(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = LogManager()
        return cls.INSTANCE

class CrawlerUtils:
    def __init__(self):
        self.config = CrawlerInit()
        self.time_now = datetime.datetime.now()
        
class FileExtensionFilter(Filter):
    def filter(self, record):
        record.filename = record.filename[:-3]
        record.message = '' + record.message
        return True

if __name__ == "__main__":
    log = LogManager()
    log.debug("Test")


