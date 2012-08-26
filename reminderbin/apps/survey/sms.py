__author__ = 'browsepad'

from twilio.twiml import Response
from .models import *
from reminderbin.apps.core.utils import logger, log_exception

def sms_reply(msg):
    r = Response()
    r.sms(msg)
    return r

def process_registration_request(participant):
    participant.enrolled_in_beta = True
    participant.save()
    return u'Thanks for registering. Stay tuned for invite'

def serialize_question_to_be_sent_via_sms(question):
    str_list = [question.title]
    for choice in question.Choices.all():
        str_list.append(u' (%s)%s' % (choice.simple_code, choice.text))
    return ''.join(str_list)

def process_vote_submission(char, participant):
    # question that we are expecting a response for
    question = participant.awaiting_response_on
    logger.debug('Received \'%s\' for question.pk = %d' % (char, question.pk))
    for choice in question.Choices.all():
        if char == choice.simple_code:
            # found the choice user wants to vote for
            logger.debug('\'%s\' is valid choice for question.pk = %d' % (char, question.pk))
            choice.total_votes += 1
            choice.save()
            logger.debug('%s successfully voted (%s) for question (%s)' % (participant.cell, choice.text, question.title))
            question.participants.add(participant)
            question.save()
            if question.next:
                logger.debug('Next question available. question.next.pk = %d' % question.next.pk)
                return process_question_request(question.next, participant
                    #, prefix='You successfully voted (%s). '% choice.text
                    )
            else:
                logger.debug('No next question available. Requesting beta registration.')
                return u'You successfully voted (%s). End of questionnaire. Reply YES to participate in TXT4HLTH beta' % choice.text
    # this is invalid entry. return
    return u'Error: Invalid entry. %s' % serialize_question_to_be_sent_via_sms(question)

def get_or_create_participant(cell):
    participants = Participant.objects.filter(cell=cell)
    if participants.exists() and len(participants) is not 0:
        participant = participants[0]
    else:
        participant = Participant.objects.create(cell=cell)
        participant.save()
    return participant

def process_message(body, participant):
    feedback = Feedback.objects.create(message=body, provided_by=participant)
    logger.debug('Feedback saved: from = %s, body = %s' % (feedback.provided_by.cell, feedback.message))
    #feedback.save()
    return u'Thx for your feedback -TXT4HLTH'

def process_question_request(question, participant, prefix=''):
    participant.awaiting_response_on = question
    participant.save()
    logger.debug('Successfully saved participant.awaiting_response_on.pk to %d' % participant.awaiting_response_on.pk)
    serialized_question = serialize_question_to_be_sent_via_sms(question)
    logger.debug('Sending question to user = %s: %s' % (participant.cell, serialized_question))
    #feedback.save()
    return u'%s%s' % (prefix, serialized_question)

def process_sms(body, from_phone):
    try:
        logger.info('INCOMING SMS: from = %s, body = %s' % (from_phone, body))

        # add or retrieve participant to the db
        participant = get_or_create_participant(from_phone)

        if body.startswith('YES'):
            # user wants to register
            logger.debug('User wants to enrol in BETA')
            response = process_registration_request(participant)
        elif body.isdigit():
            digit = int(body)
            question = find_question(digit)
            if question:
                logger.debug('User sent %d to answer question = %s' % (digit, question.title))
                response = process_question_request(question, participant)
            else:
                logger.info('User sent %d which isnt pk for any question. Returning error' % digit)
                response = u'Error: Incorrect survey id. Please retry. - TXT4HLTH'
        elif body in valid_choice_codes():
            response = process_vote_submission(body, participant)
        elif body[0].isdigit() is False:
            # user sent a message to be displayed in the ticket
            logger.debug('User wants to submit feedback = %s' % body)
            response = process_message(body, participant)
        else:
            # user sent a numeric code
            logger.debug('User wants to vote = %s' % body)
            response = process_vote_submission(body, participant)
    except Exception, e:
        log_exception('Exception processing incoming error message')
        response = u'Error: An application error occurred. Please try again later. Sorry! -TXT4HLTH'
    logger.info('OUTGOING SMS: %s' % response)
    return response