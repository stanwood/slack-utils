# import json
#
#
# def test_correct_sent_message(app, taskqueue, mock_requests):  # TODO: Fix webtest
#     payload = {
#         'message': 'Hello world',
#         'channel': '#hello_world'
#     }
#
#     response = app.post('/_ah/queue/slack', params=json.dumps(payload))
#
#     tasks = taskqueue.GetTasks(queue_name='slack')
#
#     assert len(tasks) == 1
