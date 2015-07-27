from pkg_resources import get_distribution

__project__ = 'sky'
try:
    __version__ = get_distribution(__project__).version
except:
    __version__ = "0.0.0"

from .capsule import Capsule    
from .dbpedia import get_dbpedia_from_words
from .multi import *
from .helper import *
