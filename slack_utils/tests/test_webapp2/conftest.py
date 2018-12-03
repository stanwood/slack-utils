import os

import pytest

import webtest
import webapp2


@pytest.fixture
def testbed():
    from google.appengine.ext import testbed
    base_dir = os.path.abspath((os.path.dirname(__file__)))
    tb = testbed.Testbed()
    tb.activate()
    tb.init_app_identity_stub()
    tb.init_datastore_v3_stub()
    tb.init_memcache_stub()
    tb.init_urlfetch_stub()
    tb.init_app_identity_stub()
    tb.init_search_stub()

    tb.init_taskqueue_stub(root_path=os.path.join(base_dir, '..'))
    tb.MEMCACHE_SERVICE_NAME = testbed.MEMCACHE_SERVICE_NAME
    tb.TASKQUEUE_SERVICE_NAME = testbed.TASKQUEUE_SERVICE_NAME

    yield tb

    tb.deactivate()


@pytest.fixture
def taskqueue(testbed):
    yield testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)


@pytest.fixture
def app(testbed):
    from slack_utils.gae.queue import SlackQueueHandler
    app = webapp2.WSGIApplication(
        (
            webapp2.Route(r'/_ah/queue/slack', SlackQueueHandler),
        ),
    )

    return webtest.TestApp(app)
