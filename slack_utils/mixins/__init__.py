import abc
import logging

from slack import (
    config,
    client
)
from slack.errors import (
    SlackMixinError
)


class Base(object):
    @abc.abstractproperty
    def slack_tokens(self):
        pass

    @property
    def slack(self):
        return client.Slack(*self.slack_tokens)

    @property
    def admin_im_channel(self):
        return self.slack.request('im.open', {'user': config.SLACK_ADMIN_USER_ID})['channel']['id']

    @property
    def slack_users(self):
        return self.slack.request('users.list')

    def get_slack_user_id_by_name(self, user_name):
        try:
            return [user for user in self.slack_users['members'] if user_name == user.get('real_name')][0]
        except IndexError:
            message = "Could not find user by name {} in Slack directory".format(user_name)
            raise SlackMixinError(message)

    def get_slack_user_id_by_mail(self, email):
        try:
            user = filter(lambda m: m['profile'].get('email') == email, self.slack_users['members'])[0]
        except IndexError:
            logging.warning(
                u'Not able to match {} mail from jira with any slack user.'.format(
                    email,
                )
            )
            return None
        else:
            return user['id']

    def open_channel(self, users):

        users = set(users) - set(config.SLACK_IGNORE_USERS_IDS)
        users.discard(None)

        if len(users) == 1:
            response = self.slack.request(
                'im.open',
                {
                    'user': users.pop()
                }
            )
        elif len(users) > 1:
            response = self.slack.request(
                'mpim.open',
                {
                    'users': ','.join(users)
                }
            )
        else:
            raise SlackMixinError('Cannot create channel. Users list empty')

        try:
            return response['channel']['id']
        except KeyError:
            pass

        try:
            return response['group']['id']
        except KeyError:
            raise SlackMixinError("Could not open dm channel: {}".format(response))

    def admin_message(self, message):
        self.slack.request(
            'chat.postMessage',
            {
                'channel': self.open_channel([config.SLACK_ADMIN_USER_ID]),
                'text': message
            }
        )
