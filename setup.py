import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pybeats",
    version = "0.1.1",
    author = "Teja Vishwanadha",
    author_email = "teja@beatsmusic.com",
    description = ("Beats Music SDK"),
    license = "BSD",
    keywords = "daisy mog beats beatsmusic sdk",
    url = "http://developer.beatsmusic.com",
    packages=[
        'pybeats',
        'pybeats.model'
    ],
    install_requires=[
        "requests >= 2.3.0"
    ],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio"
    ],
)
