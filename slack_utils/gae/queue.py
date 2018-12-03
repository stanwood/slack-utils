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
