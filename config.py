import os

# Creating directory
dir_path = f'{os.getcwd()}/data'

if not os.path.exists(dir_path):
    os.mkdir(dir_path)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-special-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.getcwd()}/data/app.db'
    # SQLALCHEMY_BINDS = {'cards': '/Users/vcorvinus/PycharmProjects/far_parsers/data/cards.db'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
