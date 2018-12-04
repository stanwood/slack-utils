import logging
import urllib

import webapp2

from slack_utils.gae.models import SlackAuthRequest


class AuthorizeHandler(webapp2.RequestHandler):

    SCOPES = ''
    AUTHORIZE_URL = ''
    CALLBACK_URI_NAME = ''
    CLIENT_ID = ''

    def get(self):
        state = SlackAuthRequest.save_state()

        redirect_url = '{}{}'.format(self.request.host_url, webapp2.uri_for(self.CALLBACK_URI_NAME))
        logging.info(redirect_url)
        params = {
            'client_id': self.CLIENT_ID,
            'scope': self.SCOPES,
            'redirect_uri': redirect_url,
            'state': state,
        }
        self.redirect('{}?{}'.format(self.AUTHORIZE_URL, urllib.urlencode(params)))
