#!/usr/bin/env python

from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = None

setup(
    name='isobar',
    version='0.0.3',
    description='An isobar fork using mido library instead of python-rtmidi',
    long_description=long_description,
    author='Daniel Jones',
    author_email='dan-isobar@erase.net',
    url='https://github.com/faroit/isobar',
    packages=['isobar'],
    install_requires=['pyOSC >= 0.3b0', 'mido'],
    keywords=('sound', 'music', 'composition'),
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Artistic Software',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ]
)
