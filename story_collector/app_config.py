import os

DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PW = os.getenv('MYSQL_PASSWORD', '')
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_NAME = os.getenv('MYSQL_DB', 'story_collector')

ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'something-secret')

USE_FAKE_DATA = os.getenv('USE_FAKE_DATA', True) # set this to True to use dummy data instead of db