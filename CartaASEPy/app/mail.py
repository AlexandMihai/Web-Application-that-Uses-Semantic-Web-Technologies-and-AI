from flask_mail import Message
from . import mail

def send_reset_email(user_email, reset_code):
    msg = Message("Your Password Reset Code", recipients=[user_email])
    msg.body = f"Your password reset code is: {reset_code}"
    mail.send(msg)
