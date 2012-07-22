from celery.task import task
from celery.task import periodic_task
from django.core.cache import cache
from time import sleep

from datetime import timedelta
from celery.decorators import task, periodic_task
from django.utils import timezone

from .models import *
from .utils import *

from reminderbin.apps.core.utils import *

# Run this
# python manage.py celeryd -E -B --loglevel=INFO

@periodic_task(run_every=timedelta(minutes=1))
def send_all_pending_sms():
    try:
        pending_reminders = [reminder for reminder in Reminder.objects.all()
                             if reminder.when < timezone.now()
        and reminder.sms_status is not Reminder.DELIVERED_STATUS]
        for pending_reminder in pending_reminders:
            try:
                send_sms(pending_reminder.appointment.patient.cell,
                    pending_reminder.appointment.patient.name,
                    '%s - appointment reminder. -TXT4HLTH' % pending_reminder.appointment.patient.name)
                pending_reminder.sms_status = Reminder.DELIVERED_STATUS
                pending_reminder.save() # real save to DB.
            except TwilioRestException, te:
                log_exception("Exception while sending sms to %s" % pending_reminder.appointment.patient.cell)
            except Exception, e:
                log_exception("Exception while sending sms to %s" % pending_reminder.appointment.patient.cell)
            logger.info("Sent reminder to %s" % pending_reminder.appointment.patient.cell)
    except Exception, e:
        log_exception("Exception while executing send_all_pending_sms task asynchronously. %s" % e)
        raise e