__author__ = 'browsepad'

from twilio.twiml import Response


def sms_reply(request, to, msg):
    r = Response()
    r.sms(msg)
    return r

