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
