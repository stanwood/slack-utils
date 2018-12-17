# The MIT License (MIT)
# 
# Copyright (c) 2018 stanwood GmbH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
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

    def request(self, method, message=None, headers=None, url=None):
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
            url=url or self.BASE_URL + method,
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

    def update_message(self, message, url=None):
        return self.request('chat.update', message, url=None)

    def delete_message(self, message):
        return self.request('chat.delete', message)

    def post_ephemeral_message(self, payload):
        logging.debug(payload)
        return self.request('chat.postEphemeral', payload)

    def get_message_permalink(self, payload):
        return self.request('chat.getPermalink', payload)

    def set_user_status(self, message):
        return self.request('users.profile.set', message)

    def set_dnd_snooze(self, message):
        return self.request('dnd.setSnooze', message)

    def get_user_presence(self, message):
        return self.request('users.getPresence', message)

    def search_message(self, message):
        """
        API Reference:
            https://api.slack.com/methods/search.messages
        """
        message['as_user'] = True
        return self.request('search.messages', message)

    def get_user_profile(self):
        return self.request(
            'users.profile.get',
            {
                'as_user': True,
            }
        )

    def user_info(self, user_id):
        return self.request('users.info', {'user': user_id})
