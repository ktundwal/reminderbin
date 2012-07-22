from celery.task import task
from celery.task import periodic_task
from django.core.cache import cache
from time import sleep

from datetime import timedelta
from celery.decorators import periodic_task
from django.utils import timezone

from .models import *
from .utils import *

from reminderbin.apps.core.utils import *

# Run this
# python manage.py celeryd -E -B --loglevel=INFO

def log_exception(logger, message=''):
    '''
    logs stacktrace with function name.
    usage:
        import traceback
        log_exception(message='some message goes here')
    '''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    lines.append(message)
    logger.error(''.join('!! ' + line for line in lines))  # Log it or whatever here

@periodic_task(run_every=timedelta(minutes=15))
def send_all_pending_sms():
    try:
        task_logger = send_all_pending_sms.get_logger()
        task_logger.info("********* Current UTC Time = %s *********" % timezone.now())
        for reminder in Reminder.objects.all():
            task_logger.info("    Reminder: %s at %s status = %d" % (reminder.appointment.patient.cell, reminder.when, reminder.sms_status))
        pending_reminders = [reminder for reminder in Reminder.objects.all()
                             if reminder.when < timezone.now()
        and reminder.sms_status is not Reminder.DELIVERED_STATUS]
        task_logger.info("    Due reminders = %d" % len(pending_reminders))
        for pending_reminder in pending_reminders:
            try:
                send_sms(pending_reminder.appointment.patient.cell,
                    pending_reminder.appointment.patient.name,
                    '%s - appointment reminder. -TXT4HLTH' % pending_reminder.appointment.patient.name)
                pending_reminder.sms_status = Reminder.DELIVERED_STATUS
                pending_reminder.save() # real save to DB.
            except TwilioRestException, te:
                log_exception(task_logger, "Exception while sending sms to %s" % pending_reminder.appointment.patient.cell)
            except Exception, e:
                log_exception(task_logger, "Exception while sending sms to %s" % pending_reminder.appointment.patient.cell)
            task_logger.info("    Sent reminder to %s" % pending_reminder.appointment.patient.cell)
    except Exception, e:
        log_exception(task_logger, "Exception while executing send_all_pending_sms task asynchronously. %s" % e)
        raise e