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
import json
import os

import webapp2
from google.appengine.api import taskqueue

from slack_utils.mixins.queue import BaseQueueHandler


class SlackQueueHandler(webapp2.RequestHandler, BaseQueueHandler):
    @property
    def slack_tokens(self):
        return os.environ.get('SLACK_BOT_TOKEN', None), os.environ.get('SLACK_APP_TOKEN', None)

    @property
    def queue(self):
        queue = os.environ.get('SLACK_QUEUE', 'default')
        return taskqueue.Queue(queue)

    @property
    def messages(self):
        return self.request.json

    @staticmethod
    def create_task(payload, **kwargs):
        return taskqueue.Task(
            payload=json.dumps(payload),
            **kwargs
        )
