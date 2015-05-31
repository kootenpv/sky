from setuptools import setup

MAJOR_VERSION = '0'
MINOR_VERSION = '0'
MICRO_VERSION = '72'
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(name = 'sky',
      version = VERSION,
      description = 'sky -- AI powered scraping',
      url = 'https://github.com/kootenpv/sky',
      author = 'Pascal van Kooten',
      author_email = 'kootenpv@gmail.com',
      license = 'GPL',
      packages = ['sky'],
      install_requires = [ 
          'lxml',
          'selenium'
      ], 
      zip_safe = False)
