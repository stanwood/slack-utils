import os


SLACK_ADMIN_USER_ID = os.environ.get('SLACK_ADMIN_USER_ID')
SLACK_IGNORE_USERS_IDS = os.environ.get('SLACK_IGNORE_USERS_IDS', '').split(',')
SLACK_TEAM = os.environ.get('SLACK_TEAM')
