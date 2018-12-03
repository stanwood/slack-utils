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
