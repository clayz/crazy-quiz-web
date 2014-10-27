import urllib
from google.appengine.api import urlfetch


class GCMSender:
    def __init__(self, api_key):
        self.api_key = api_key

    def push(self, push_tokens=None, data=None):
        from main import app

        url = 'https://android.googleapis.com/gcm/send'

        form_fields = {
            "data": {
                "score": "5x1",
                "time": "15:10"
            },
            "registration_ids": [
                'APA91bEFDC6KBdrujA8y8OVlHSvQsasMNZITDEQIcMnngkvPw5ro5MhcXlOhkX5BI1iyQclOBVT5NzM0SoFsbLnF2gQY0qcC8QSfFzP1T3NVU0D6PwpRYozHL3O91MZAqn_deUCKqbVV8SNAnSv12559y6TvcY39kQ']
        }

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url,
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Authorization': 'AIzaSyDT9ZvSZbdMtegBPr4w3y8qdcRgwk4mIhI',
                                         'Content-Type': 'application/json'})

        app.logger.info(result.status_code)
        app.logger.info(result.content)


class APNSSender:
    def __init__(self, certification, password):
        self.certification = certification
        self.password = password