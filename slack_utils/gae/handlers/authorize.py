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
