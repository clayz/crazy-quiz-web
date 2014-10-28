import json
from google.appengine.api import urlfetch
from constants import GAE_API_KEY


def gcm_push(push_tokens, title, message):
    from main import app

    url = 'https://android.googleapis.com/gcm/send'
    data = {
        "registration_ids": push_tokens,
        "data": {
            "title": title,
            "message": message
        }
    }

    result = urlfetch.fetch(url=url, payload=json.dumps(data), method=urlfetch.POST,
                            headers={'Authorization': 'key=%s' % GAE_API_KEY,
                                     'Content-Type': 'application/json'})

    app.logger.debug('Result status code: %d, content: %s' % (result.status_code, result.content))