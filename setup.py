from distutils.core import setup
import py2exe



setup(
    windows=[{'script': 'application.py'}],
    options={
        'py2exe': 
        {
            'includes': ['lxml.etree', 'lxml._elementpath'],
        }
    }
)
