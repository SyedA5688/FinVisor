import os


class Config:
    SECRET_KEY = os.environ.get('FV_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FV_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('FV_EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('FV_EMAIL_PASS')

