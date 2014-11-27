import json
import time
from google.appengine.api import urlfetch
from constants import GAE_API_KEY
from apns import APNs, Frame, Payload


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


def apns_push():
    from main import app

    def response_listener(error_response):
        app.logger.info("Client get error response: %s" % str(error_response))

    apns_enhanced = APNs(use_sandbox=True, cert_file='res/apns/apns-development.pem', enhanced=True)
    apns_enhanced.gateway_server.register_response_listener(response_listener)

    payload = Payload(alert="Hello World!", sound="default", badge=1)
    frame = Frame()
    identifier = 1
    expiry = time.time() + 3600
    priority = 10
    frame.add_item('c20e97a561c44aac9b70e8a9bc07b8e5b83ff753cbc39e09e93684a46e35a40a', payload, identifier, expiry, priority)
    apns_enhanced.gateway_server.send_notification_multiple(frame)
