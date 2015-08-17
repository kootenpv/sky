from pkg_resources import get_distribution

__project__ = 'sky'
try:
    __version__ = get_distribution(__project__).version
except:
    __version__ = "0.0.93"

from .dbpedia import get_dbpedia_from_words
from .helper import *
