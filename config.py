import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                         "sqlite:////tmp/test.db")

MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "noreply@example.com")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
MAIL_SENDER_EMAIL = os.environ.get("MAIL_SENDER_EMAIL", MAIL_USERNAME)
MAIL_SUPPRESS_SEND = os.environ.get("MAIL_SUPPRESS_SEND", False)

SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:5000")
PREFERRED_URL_SCHEME = os.environ.get("PREFERRED_URL_SCHEME", "http")
