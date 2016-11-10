from datetime import datetime

# this is for developing the interface w/o setting up the database and stuff

date_format = '%Y-%m-%d %H:%M:%S.%f'

FAKE_STORIES = [
    {
        'id': 1,
        'call_sid': 'CAf0c70fdde85509666833ebec4077c9b3',
        'from_number': '+19787600972',
        'recording_url': 'https://api.twilio.com/2010-04-01/Accounts/AC8820553f8206a5c5f7608355621ccd90/Recordings/RE257375633d2a49533122e184f1330061',
        'is_approved': False,
        'dt': datetime.strptime('2016-11-07 16:06:22.387488', date_format),
        'caller_zip': '94103'
    }
]