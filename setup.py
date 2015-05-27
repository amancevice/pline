import os
from setuptools import setup

NAME    = 'pline'
VERSION = '0.0.1'
AUTHOR  = 'amancevice'
EMAIL   = 'smallweirdnum@gmail.com'
DESC    = 'AWS Data Pipeline Wrapper'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup( name                 = NAME,
       version              = VERSION,
       author               = AUTHOR,
       author_email         = EMAIL,
       packages             = [ NAME ],
       package_data         = { "%s" % NAME : ['README.md'] },
       include_package_data = True,
       url                  = 'http://www.smallweirdnumber.com',
       description          = DESC,
       long_description     = read('README.md'),
       install_requires     = [ "boto",
                                "nose",
                                "mock" ],
       test_suite           = "nose.collector" )