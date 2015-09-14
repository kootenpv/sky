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

    def __init__(self, project_name, server, keys_to_save=None):
        logging.Handler.__init__(self)
        self.project_name = project_name
        self.server = server
        if keys_to_save is None:
            keys_to_save = ['name', 'levelname', 'dbtime', 'message', 'exc_text']
        self.keys_to_save = keys_to_save

    def formatDBTime(self, record):
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

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

    def save_log(self, log_line_dict):
        print(':'.join([log_line_dict[k] for k in self.keys_to_save if log_line_dict[k]]))


class CloudantLogger(Logger):
    """ het grote probleem is dat ik veel te veel zou gaan loggen, db kan dat niet aan """

    def save_log(self, log_line_dict):
        print(':'.join([log_line_dict[k] for k in self.keys_to_save if log_line_dict[k]]))


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
