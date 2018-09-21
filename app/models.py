from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(128),unique=True)
    password =db.Column(db.String(128))
    # 一对多的关系中，要在一这一面建立关系view
    # 在定义关系时，第一个参数是建立关系的数据表的类名Post，要大写
    posts = db.relationship('Post',backref = 'author',lazy = 'dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(256))
    title = db.Column(db.String(64),index=True,unique=True)
    timestamp =db.Column(db.DateTime,default=datetime.utcnow)
    #In the "many" part db.ForeignKey use the table name 'user'
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.title)