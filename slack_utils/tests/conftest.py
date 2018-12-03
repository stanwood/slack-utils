import mock
import pytest


@pytest.fixture
def mock_requests():
    with mock.patch('slack_utils.client.requests') as mock_requests:
        mock_response = mock.MagicMock(status_code=200, content='123')
        mock_response.json.return_value = {'ok': True}
        mock_requests.post.return_value = mock_response
        yield mock_requests
