import os

class Config(object):
    # SECRET_KEY = os.environ.get("Secret_key")
    SECRET_KEY = os.urandom(32)