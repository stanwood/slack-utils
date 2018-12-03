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
