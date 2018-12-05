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
import abc
import json

from slack_utils import mixins


class BaseQueueHandler(mixins.Base):
    """
    Base class for sending slack message using queue task.
    """

    LIMIT = 4

    @abc.abstractproperty
    def queue(self):
        pass

    @abc.abstractproperty
    def messages(self):
        pass

    @abc.abstractmethod
    def create_task(self, payload, **kwargs):
        pass

    def send_message(self, tasks, **kwargs):
        self.queue.add(
            tasks,
            **kwargs
        )

    def post(self):

        messages = self.messages

        if isinstance(messages, dict):
            thread = messages.pop('_thread', [])
            response = self.slack.post_message(messages)

            if thread:
                for message in thread:
                    message['thread_ts'] = response['ts']

                self.send_message(thread, transactional=True)

            return

        tasks = [
            self.create_task(
                json.dumps(message),
            )
            for message in messages[:self.LIMIT]
        ]

        messages = messages[self.LIMIT:]

        if messages:
            tasks.append(
                self.create_task(
                    json.dumps(messages),
                    url='/_ah/queue/slack',
                )
            )

        self.send_message(
            tasks,
            transactional=True,
        )
