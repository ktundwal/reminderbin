__author__ = 'browsepad'

from django.utils import unittest
from reminderbin.apps.survey.models import *
from datetime import timedelta
from reminderbin.apps.survey.sms import *
from django.utils.timezone import now

class SmokeTestCase(unittest.TestCase):
    """
    Load question, choices and mock receiving SMS
    (reminderbin)$ python manage.py test survey
    """
    def setUp(self):

        # first question
        self.question1 = Question.objects.create(
            title = 'Did sonu play?',
            text = 'as in outside',
            start = now(),
            end = now() + timedelta(days=1))
        question1_choice_yes = Choice.objects.create(question = self.question1, text = 'yes')
        question1_choice_no = Choice.objects.create(question = self.question1, text = 'no')

        # second question
        self.question2 = Question.objects.create(
            title = 'What did she play?',
            text = 'as in game',
            start = now(),
            end = now() + timedelta(days=1))
        question2_choice_football = Choice.objects.create(question = self.question2,text = 'football')
        question2_choice_cricket = Choice.objects.create(question = self.question2,text = 'cricket')
        question2_choice_tennis = Choice.objects.create(question = self.question2,text = 'tennis')

        # tie them together
        self.question1.next = self.question2
        self.question1.save()

        self.participant1 = '+13030001111'
        self.participant2 = '+13030002222'

    def get_participant(self, cell):
        participants = Participant.objects.filter(cell=cell)
        self.assertTrue(participants.exists() and len(participants) is not 0, msg='Failed to find participant')
        participant = participants[0]
        self.assertEqual(participant.cell, cell, msg='Failed to get participants cell phone right')
        return participant

    def test_running_questionnaire(self):
        """Participant can run through questionnaire from start to finish"""
        request = '%s' % self.question1.pk
        logger.info('REQUEST : %s' % request)
        response = process_sms(request, self.participant1)
        self.assertFalse(response.startswith(u'Error:'), msg='Error retrieving first question of the survey')
        logger.info('RESPONSE: %s' % response)

        # cell must have registered with system. find it.
        participant = self.get_participant(self.participant1)

        self.assertEqual(participant.awaiting_response_on.pk, self.question1.pk,
            'System didnt record what question are we waiting for user to reply')

        # test valid entry
        request = '%s' % 'a'
        logger.info('REQUEST : %s' % request)
        response = process_sms(request, self.participant1)
        self.assertFalse(response.startswith(u'Error:'), msg='Error selecting choice a of first question')
        logger.info('RESPONSE: %s' % response)

        participant = self.get_participant(self.participant1)

        self.assertEqual(participant.awaiting_response_on.pk, self.question2.pk,
            'System didnt record second question as the one we are expecting %s to reply back' % participant.cell)

        # test invalid entry
        request = '%s' % 'v'
        logger.info('REQUEST : %s' % request)
        response = process_sms(request, self.participant1)
        self.assertTrue(response.startswith(u'Error:'), msg='No error reported for invalid entry')
        logger.info('RESPONSE: %s. Invalid entry test PASSED' % response)

        # test invalid entry
        request = '%s' % '123'
        logger.info('REQUEST : %s' % request)
        response = process_sms(request, self.participant1)
        self.assertTrue(response.startswith(u'Error:'), msg='No error reported for invalid entry')
        logger.info('RESPONSE: %s. Invalid entry test PASSED' % response)

        # test valid entry
        request = '%s' % 'b'
        logger.info('REQUEST : %s' % request)
        response = process_sms(request, self.participant1)
        self.assertFalse(response.startswith(u'Error:'), msg='Error selecting choice b of second question')
        logger.info('RESPONSE: %s. Valid entry test PASSED' % response)

        request = '%s' % 'YES'
        logger.info('REQUEST : %s' % request)
        response = process_sms(request, self.participant1)
        self.assertFalse(response.startswith(u'Error:'), msg='Error registering for beta')
        self.assertTrue(self.get_participant(self.participant1).enrolled_in_beta, msg='Error registering for beta')
        logger.info('RESPONSE: %s. Request for beta registration PASSED' % response)