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
def queue_app(testbed):
    from slack_utils.gae.queue import SlackQueueHandler
    app = webapp2.WSGIApplication(
        (
            webapp2.Route(r'/_ah/queue/slack', SlackQueueHandler),
        ),
    )

    return webtest.TestApp(app)
