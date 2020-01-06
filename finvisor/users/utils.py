from flask_mail import Message
from finvisor import mail
from flask import url_for


def send_reset_email(user): # Method to send email
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='finvisorRE@gmail.com', recipients=[user.email])
    msg.body = f'''To reset password, click the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not try resetting your password or this is not you, please ignore this message.
    '''
    mail.send(msg)

