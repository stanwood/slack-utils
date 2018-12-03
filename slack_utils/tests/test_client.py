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
import mock
import pytest


def test_client_request(mock_requests):
    from slack_utils import client

    slack = client.Slack('', '')

    results = slack.request('method')
    assert results['ok'] is True
    assert mock_requests.post.call_count == 1


def test_client_request_400_status_code(mock_requests):
    mock_response = mock.MagicMock(status_code=400, content='123')
    mock_response.json.return_value = {'ok': True}
    mock_requests.post.return_value = mock_response

    from slack_utils import client
    from slack_utils import errors

    slack = client.Slack('', '')
    with pytest.raises(errors.SlackError):
        slack.request('method')


def test_client_request_content_not_ok(mock_requests):
    mock_response = mock.MagicMock(status_code=200, content='123')
    mock_response.json.return_value = {'ok': False}
    mock_requests.post.return_value = mock_response

    from slack_utils import client
    from slack_utils import errors

    slack = client.Slack('', '')
    with pytest.raises(errors.SlackError):
        slack.request('method')


def test_client_request_content_not_ok_rate_limit(mock_requests):
    mock_response = mock.MagicMock(status_code=200, content='123')
    mock_response.json.return_value = {'ok': False, 'error': 'ratelimited'}
    mock_requests.post.return_value = mock_response

    from slack_utils import client
    from slack_utils import errors

    slack = client.Slack('', '')
    with pytest.raises(errors.SlackLimitRateError):
        slack.request('method')
