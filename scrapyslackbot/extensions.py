# -*- coding: utf-8 -*-

import socket
from datetime import datetime, timedelta, timezone

from scrapy import signals
from scrapy.exceptions import NotConfigured
from slackclient import SlackClient


class SlackBot(object):

    def __init__(self, stats, slack_bot_token, channel):
        self.stats = stats
        self.bot = SlackClient(slack_bot_token)
        self.channel = channel

    @classmethod
    def from_crawler(cls, crawler):
        slack_bot_token = crawler.settings.get('SLACK_BOT_TOKEN')
        channel = crawler.settings.get('SLACK_CHANNEL')
        if not crawler.settings.getbool('SLACK_ENABLED') or not slack_bot_token or not channel:
            raise NotConfigured
        ext = cls(crawler.stats, slack_bot_token, channel)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_opened(self, spider):
        attachments = [
            {
                'fallback': 'Spider opened',
                'color': 'good',
                'author_name': socket.getfqdn(),
                'title': 'Spider opened',
                'footer': spider.name,
                'footer_icon': 'https://scrapy.org/favicons/favicon-16x16.png',
                'ts': self.stats.get_value('start_time').replace(tzinfo=timezone(timedelta(hours=0))).timestamp()
            }
        ]
        self.bot.api_call('chat.postMessage', channel=self.channel, attachments=attachments)

    def spider_closed(self, spider, reason):
        attachments = [
            {
                'fallback': 'Spider closed',
                'color': 'good',
                'author_name': socket.getfqdn(),
                'title': 'Spider closed',
                'fields': [
                    {
                        'title': 'Reason',
                        'value': reason,
                        'short': False
                    },
                    {
                        'title': 'Item Scraped Count',
                        'value': self.stats.get_value('item_scraped_count') if self.stats.get_value(
                            'item_scraped_count') is not None else 0,
                        'short': False
                    },
                    {
                        'title': 'Filtered',
                        'value': self.stats.get_value('dupefilter/filtered') if self.stats.get_value(
                            'dupefilter/filtered') is not None else 0,
                        'short': False
                    }
                ],
                'footer': spider.name,
                'footer_icon': 'https://scrapy.org/favicons/favicon-16x16.png',
                'ts': self.stats.get_value('finish_time').replace(tzinfo=timezone(timedelta(hours=0))).timestamp()
            }
        ]
        self.bot.api_call('chat.postMessage', channel=self.channel, attachments=attachments)

    def spider_error(self, failure, response, spider):
        attachments = [
            {
                'fallback': 'Spider error',
                'color': 'bad',
                'author_name': socket.getfqdn(),
                'title': 'Spider error',
                'fields': [
                    {
                        'title': 'Error',
                        'value': failure.getErrorMessage(),
                        'short': False
                    }
                ],
                'footer': spider.name,
                'footer_icon': 'https://scrapy.org/favicons/favicon-16x16.png',
                'ts': datetime.now().timestamp()
            }
        ]
        self.bot.api_call('chat.postMessage', channel=self.channel, attachments=attachments)
