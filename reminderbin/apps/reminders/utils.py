__author__ = 'ktundwal'

from reminderbin.apps.core.utils import *

from twilio import twiml
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

import reminderbin

def send_sms(phone, name, msg):
    try:
        client = TwilioRestClient(
            reminderbin.settings.TWILIO_ACCOUNT_SID,
            reminderbin.settings.TWILIO_AUTH_TOKEN)
        message = client.sms.messages.create(to=phone,
            from_=reminderbin.settings.TWILIO_CALLER_ID,
            body=name + ', ' + msg)
        logger.info('Sent SMS - %s - to %s. Response - %s' % (msg,phone,message))
    except TwilioRestException,te:
        log_exception('Unable to send SMS message!')
