import yumroad
from flask_mail import Message
from yumroad.extensions import mail

DEFAULT_FROM = ('Yumroad', 'foxv.boutique@gmail.com')

def send_basic_welcome_message(recipient_email):
    message = Message('Welcome to Yumroad',
                        sender=DEFAULT_FROM,
                        # sender=yumroad.config.
                        recipients=[recipient_email],
                        body='Thank for joining. Let us know if you have any question!'
                    )
    mail.send(message)