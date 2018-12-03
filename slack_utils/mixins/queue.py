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
