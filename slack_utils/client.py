import logging
import unicodedata
import urllib

import requests

from slack_utils.errors import (
    SlackError,
    SlackLimitRateError,
)


class Slack(object):
    BASE_URL = 'https://slack.com/api/'

    def __init__(self, bot_token, app_token):
        if isinstance(bot_token, unicode):
            bot_token = bot_token.encode('ascii')
        if isinstance(app_token, unicode):
            app_token = app_token.encode('ascii')

        self.bot_token = bot_token
        self.app_token = app_token

    @staticmethod
    def _normalize_unicode(text):
        return str(unicodedata.normalize('NFKD', text).encode('ascii', 'ignore'))

    @classmethod
    def _normalize_values(cls, input_value):

        if isinstance(input_value, unicode):
            return cls._normalize_unicode(input_value)

        elif isinstance(input_value, list):
            return [cls._normalize_values(v) for v in input_value]

        elif isinstance(input_value, dict):
            return {
                str(key): cls._normalize_values(value)
                for key, value in input_value.iteritems()
            }

        else:
            return input_value

    def request(self, method, message=None, headers=None):
        if message is None:
            message = {}
        if headers is None:
            headers = {}

        if message.get('as_user'):
            message['token'] = self.app_token
        else:
            message['token'] = self.bot_token

        message = self._normalize_values(message)

        logging.debug('POST {} {}'.format(method, message))

        response = requests.post(
            url=self.BASE_URL + method,
            data=urllib.urlencode(message),
            headers=headers,
        )
        logging.debug('Response: {}'.format(response.content))
        if response.status_code / 400:
            raise SlackError(response.content)

        content = response.json()
        if content.get('ok', False) is False:
            if content.get('error') == 'ratelimited':
                raise SlackLimitRateError(response.content)

            else:
                raise SlackError(content.get('error', 'Error field not found'))

        return response.json()

    def post_message(self, message):
        return self.request('chat.postMessage', message)

    def update_message(self, message):
        return self.request('chat.update', message)

    def delete_message(self, message):
        return self.request('chat.delete', message)
