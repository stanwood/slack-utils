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

import webapp2
from google.appengine.api import memcache

from slack_utils import (
    config,
    client,
    mixins
)
from slack_utils.gae.models import SlackToken


class SlackMixin(mixins.Base):
    USERS_CACHE_TTL = 60 * 60 * 3

    @property
    def slack_tokens(self):
        return SlackToken.get_team_tokens(config.SLACK_TEAM)

    @webapp2.cached_property
    def slack(self):
        return client.Slack(*self.slack_tokens)

    @webapp2.cached_property
    def slack_users(self):
        memcache_key = 'slack:users.list'
        slack_users = memcache.get(memcache_key)
        if not slack_users:
            slack_users = self.slack.request('users.list')
            memcache.set(memcache_key, slack_users, time=self.USERS_CACHE_TTL)
        else:
            logging.debug('Cached slack users')

        return slack_users

    @webapp2.cached_property
    def admin_im_channel(self):
        return super(SlackMixin, self).admin_im_channel
