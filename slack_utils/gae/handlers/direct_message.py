import logging
import webapp2

from slack_utils.gae.webapp2_utils import SlackMixin


class SlackDirectMessageHandler(webapp2.RequestHandler, SlackMixin):

    @property
    def channel(self):
        return self.request.get('channel')

    @webapp2.cached_property
    def message(self):
        return self.request.get('message')

    def post(self):
        logging.debug(u"Posting {} to channel {}".format(
            self.message,
            self.channel
        ))
        self.slack.request(
            'chat.postMessage',
            {
                'channel': self.channel,
                'text': self.request.get('message'),
            }
        )
