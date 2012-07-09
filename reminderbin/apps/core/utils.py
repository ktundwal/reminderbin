"""
utils
"""

import sys
import traceback
import logging

logger = logging.getLogger("reminderbin")

def log_exception(message=''):
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