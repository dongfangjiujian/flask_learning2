from app import db
from datetime import datetime
# @login.user_loader修饰器在 __init__.py   login=LoginManger(app)的login中  需要先import
from app import login
from flask_login import UserMixin
# UserMixin 包含了flask login 的各种方法和属性 可以直接放在User类中实现
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(128),unique=True)
    password =db.Column(db.String(128))
    about_me = db.Column(db.String(256))

    # 一对多的关系中，要在一这一面建立关系view
    # 在定义关系时，第一个参数是建立关系的数据表的类名Post，要大写
    posts = db.relationship('Post',backref = 'author',lazy = 'dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

# Flask login 再session中记录登录用户，但是对用户数据库并不了解 所以需要用@login.user_loader装饰器来注册用户，让flask login能够认识到数据库
@login.user_loader
def user_loader(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(256))
    title = db.Column(db.String(64),index=True,unique=True)
    timestamp =db.Column(db.DateTime,default=datetime.utcnow)
    #In the "many" part db.ForeignKey use the table name 'user'
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.title)