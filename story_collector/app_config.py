import os

# TODO: tighten this up

# if app_config_secret.py exists, use that to set config variables
if os.path.isfile(os.path.dirname(__file__)+'/app_config_secret.py'):
    from .app_config_secret import DB_USER, DB_PW, DB_HOST, DB_NAME, ADMIN_USER, ADMIN_PASS, USE_FAKE_DATA, APP_URL

# otherwise, set config variables from environment variables, 
# & assigns them to defaults if env vars don't exist
# (this is for deploying w/ docker)
else:
    DB_USER = os.getenv('MYSQL_USER', 'root')
    DB_PW = os.getenv('MYSQL_PASSWORD', '')
    DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
    DB_NAME = os.getenv('MYSQL_DB', 'story_collector')

    ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
    ADMIN_PASS = os.getenv('ADMIN_PASS', 'something-secret')

    USE_FAKE_DATA = os.getenv('USE_FAKE_DATA', False)

    APP_URL = os.getenv('APP_URL', '')