# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext
from notification import backends

MOBILE_NUMBER_SETTING_KEY = "NOTIFICATION_TWILIO_USER_MOBILE_NUMBER"
TWILIO_ACCOUNT_SETTING_KEY = "TWILIO_ACCOUNT_SID"
TWILIO_AUTH_SETTING_KEY = "TWILIO_AUTH_TOKEN"
TWILIO_FROM_SETTING_KEY = "TWILIO_SMS_FROM_NUMBER"


def get_mobile_number(self, user):
    mobile_number_key = getattr(settings, MOBILE_NUMBER_SETTING_KEY)
    mobile_number = str(getattr(user, mobile_number_key, "0"))
    return mobile_number

class TwilioSMSBackend(backends.BaseBackend):
    spam_sensitivity = 2


    def can_send(self, user, notice_type):
        can_send = super(TwilioSMSBackend, self).can_send(user, notice_type)

        if can_send:
            if not hasattr(settings, MOBILE_NUMBER_SETTING_KEY) or
               not hasattr(settings, TWILIO_ACCOUNT_SETTING_KEY) or
               not hasattr(settings, TWILIO_AUTH_SETTING_KEY)
                return False # TODO: logging

            mobile_number = get_mobile_number(user)

            if len(mobile_number) < 7 or not mobile_number.isdigit():
                return False # TODO: logging

            return True

        return False
        

    def deliver(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            "short.txt",
            "full.txt"
        ), notice_type.label, context)

        if sender:
            from_mobile_number = getattr(settings, TWILIO_FROM_SETTING_KEY)
        else:
            from_mobile_number = get_mobile_number(sender)

        to_mobile_number = get_mobile_number(recipient)
        twilio_account = getattr(settings, TWILIO_ACCOUNT_SETTING_KEY)
        twilio_token = getattr(settings, TWILIO_AUTH_SETTING_KEY)

        client = TwilioRestClient(twilio_account, twilio_token)
        message = client.messages.create(to=to_mobile_number, from_=from_mobile_number, body=messages["short.txt"])