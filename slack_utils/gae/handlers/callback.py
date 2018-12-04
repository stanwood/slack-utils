import logging
import urllib

import requests
import webapp2

import config
from slack_utils.gae.models import SlackAuthRequest
from slack_utils.gae.models import SlackAuthRequestError
from slack_utils.gae.models import SlackToken


class SlackCallbackHandler(webapp2.RequestHandler):

    CALLBACK_URI_NAME = 'slack-callback'

    @property
    def code(self):
        return self.request.GET['code']

    @property
    def state(self):
        return self.request.GET['state']

    def get(self):
        try:
            SlackAuthRequest.validate_state(self.state)
        except SlackAuthRequestError as ex:
            self.abort(400, str(ex))

        redirect_url = '{}{}'.format(self.request.host_url, webapp2.uri_for(self.CALLBACK_URI_NAME))
        logging.info(redirect_url)
        # make a request to get permament tokens and save them
        url = 'https://slack.com/api/oauth.access?{}'.format(
            urllib.urlencode(
                {
                    'client_id': config.SLACK_CLIENT_ID,
                    'client_secret': config.SLACK_CLIENT_SECRET,
                    'code': self.code,
                    'redirect_uri': redirect_url
                }
            )
        )
        response = requests.get(
            url=url
        )
        response = response.json()
        if response['ok']:
            # store data, make sure it is not duplicated
            SlackToken.save_token(response)
            self.response.write("All set. Thanks!")
        else:
            self.response.write(response)
