# -*- coding: utf-8 -*-

from django.conf import settings
from notification import backends

MOBILE_NUMBER_SETTING_KEY = "NOTIFICATION_TWILIO_USER_MOBILE_NUMBER"

class TwilioSMSBackend(backends.BaseBackend):
    spam_sensitivity = 2

    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)

        if can_send:
            if not hasattr(settings, MOBILE_NUMBER_SETTING_KEY)
                return False # TODO: logging

            mobile_number_key = getattr(settings, MOBILE_NUMBER_SETTING_KEY)

            if not hasattr(user, mobile_number_key):
                return False # TODO: logging

            mobile_number = getattr(user, mobile_number_key)

            if len(mobile_number) < 7 or not mobile_number.isdigit():
                return False # TODO: logging

            return True

        return False
