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
