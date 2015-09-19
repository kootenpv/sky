import sys
import time
import logging

# ZODB specific
try:
    import transaction
    from BTrees.OOBTree import OOBTree
except ImportError:
    print('Optional ZODB not possible as backend. Use `pip3 install ZODB zodbpickle`')


class Logger(logging.Handler):

    def __init__(self, storage_object=None, keys_to_save=None):
        logging.Handler.__init__(self)
        self.project_name = None
        self.storage_object = storage_object
        self.plugin_name = None
        self.log = None
        if keys_to_save is None:
            keys_to_save = ['name', 'levelname', 'dbtime', 'message', 'exc_text']
        self.keys_to_save = keys_to_save

    def init_logger(self):
        raise NotImplementedError("implement 'init_logger'")

    def formatDBTime(self, record):
        record.dbtime = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created))

    def save_log(self, log_line_dict):
        raise NotImplementedError("implement 'save_log' to save: {}".format(log_line_dict))

    def emit(self, record):
        try:
            # use default formatting
            self.format(record)
            # now set the database time up
            self.formatDBTime(record)
            if record.exc_info:
                record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            else:
                record.exc_text = ""
            self.save_log(record.__dict__)
        except:
            import traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
            del ei

    def close(self):
        logging.Handler.close(self)


class StandardLogger(Logger):

    def init_logger(self):
        pass

    def save_log(self, log_line_dict):
        print(':'.join([log_line_dict[k] for k in self.keys_to_save if log_line_dict[k]]))


# class CloudantLogger(Logger):
#     """ THIS WILL NEVER WORK BECAUSE OF AIOHTTP"""
#     def init_logger(self):
#         if self.storage_object is None:
#             raise ValueError("No storage_object given; it is unclear where to store data.")

#         self.log = self.storage_object.database(self.project_name + '-crawler-log')
#         # create db if it doesnt exist
#         self.log.put()

#     def save_log(self, log_line_dict):
#         res = ':'.join([log_line_dict[k] for k in self.keys_to_save if log_line_dict[k]])
#         self.log[str(id(log_line_dict))] = res


# dh = StandardLogger('Logging', 'asdf')
# logger = logging.getLogger("")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(dh)
# logger.info("Jackdaws love my big %s of %s", "sphinx", "quartz")
# logger.debug("Pack my %s with five dozen %s", "box", "liquor jugs")

# try:
#     import math
#     math.exp(1000)
# except:
#     logger.exception("Problem with %s", "math.exp")
