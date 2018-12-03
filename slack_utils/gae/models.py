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
from google.appengine.ext import ndb

from slack_utils.errors import SlackTokenError


class SlackToken(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    access_token = ndb.StringProperty()
    scope = ndb.StringProperty()
    team_name = ndb.StringProperty()
    team_id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    bot_user_id = ndb.StringProperty()
    bot_access_token = ndb.StringProperty()
    complete_response = ndb.JsonProperty()

    @classmethod
    def save_token(cls, response):
        cls(
            id=response['user_id'],
            user_id=response['user_id'],
            access_token=response['access_token'],
            scope=response['scope'],
            team_name=response['team_name'],
            team_id=response['team_id'],
            bot_user_id=response['bot']['bot_user_id'],
            bot_access_token=response['bot']['bot_access_token'],
            complete_response=response
        ).put()

    @classmethod
    def get_bot_token(cls, team_id):
        try:
            return cls.query(cls.team_id == team_id).get().bot_access_token
        except AttributeError:
            raise SlackTokenError("Bot token not found for team {}".format(team_id))

    @classmethod
    def get_app_token(cls, team_id):
        try:
            return cls.query(cls.team_id == team_id).get().access_token
        except AttributeError:
            raise SlackTokenError("App token not found for team {}".format(team_id))

    @classmethod
    def get_team_tokens(cls, team_id):
        """
        :return: bot_token, app_token
        """
        try:
            stored_tokens = cls.query(cls.team_id == team_id).get()
            return stored_tokens.bot_access_token, stored_tokens.access_token
        except AttributeError:
            raise SlackTokenError("Tokens not found for team {}".format(team_id))

    @classmethod
    def get_user_tokens(cls, user_id):
        """
        :return: bot_token, app_token
        """
        try:
            stored_tokens = ndb.Key(cls, user_id).get()
            return stored_tokens.bot_access_token, stored_tokens.access_token
        except AttributeError:
            raise SlackTokenError("Tokens not found for user {}".format(user_id))
