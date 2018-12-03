# slack-utils

Package for sending slack messages using Slack API.
Includes mixins and utils for webapp2 and GAE.


## While using GAE

Please remember to add monkeypatch on requests-toolbelt in appengine_config.py
```python
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()
```

## Usage as git submodule

### Add submodule to the project
```bash
$ git submodule add git@github.com:stanwood/slack-utils.git lib/slack_utils
```

### Add submodule in appengine_config.py (if using App Engine)
```python
import os
from google.appengine.ext import vendor

vendor.add(os.path.join(os.path.dirname(__file__), 'lib/slack_utils'))
```

# Tests

```bash
$ cd lib/slack_utils
$ pip install -r requirements.txt
$ pytest -v slack_utils/tests/
```


# Example Usage

## Send message using Slack client

```python
from slack import client

slack_client = client.Slack('<bot_token>', '<app_token>')
slack_client.post_message('Hello world')
```

## Add queue to send slack message using any framework

1. Import _BaseQueueHandler_
    ```python
    from slack.mixins.queue import BaseQueueHandler
    ```
2. Override abstract properties and methods
3. Add your queue handler to the project routing

## Add Google App Engine queue to send slack message using webapp2

### Update _queue.yaml_ file

```yaml
queue:
- name: default
  rate: 10/s
  bucket_size: 200

- name: slack
  rate: 1/s
  bucket_size: 200
  max_concurrent_requests: 1
  retry_parameters:
    min_backoff_seconds: 60
    max_doublings: 3
    task_retry_limit: 3

```

### Add routes to your API framework (example in webapp2)

```python
import webapp2
from slack.gae.queue import SlackQueueHandler

app = webapp2.WSGIApplication(
    (
        webapp2.Route(r'/_ah/queue/slack', SlackQueueHandler),
    ),
)
```
