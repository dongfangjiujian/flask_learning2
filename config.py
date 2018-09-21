import os
basedir = os.path.abspath(os.path.dirname(__file__))
# print(os.path.join(basedir,'app.db'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MyEnglishNameIsDamon'
    # print('hello')
    SQLALCHEMY_DATEBASE_URI = os.environ.get('DATEBASE_URI') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_BINDS = {
        'users':        'mysqldb://localhost/users',
        'app':      os.environ.get('DATEBASE_URI') or 'sqlite:///' + os.path.join(basedir,'app.db')
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

