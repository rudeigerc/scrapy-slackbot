# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scrapy-slackbot',
    version='0.2.0',
    packages=['scrapyslackbot'],
    url='https://github.com/rudeigerc/scrapy-slackbot',
    license='MIT',
    author='Yuchen Cheng',
    author_email='rudeigerc@gmail.com',
    description='A Scrapy extension to send notification to the Slack channel.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['scrapy', 'slackclient'],
    keywords='scrapy slack bot',
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ]
)
