#登录扩展flask-login的应用

首先安装flask-login
pip install flask-login

初始化flask-login
在__init__.py  模块中初始化
1.先导入 from flask-login import LoginManger
2,login = LoginManger(app)

flask-login 关于用户的属性和方法都包含在UserMixin中，可以作为User模型的参数来应用
在应用先 需要先进行导入  from flask-login import UserMixin
eg： class User(UserMixin,db.Model):
        ...

主要用到的方法和属性有  current_user（is_authenticated,is_anonymous)，login_user,logout_user
由于flask-login用对登录用户进行追踪（current_user),而又对数据库不了解，所以需要每次将登陆用户的id值传给login控制柄，以获得用户信息.这里需要用到@login.user_loader装饰器
route.py
from app import login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

login_user的应用
1. from flask-login import login_user
2. 判断登录语句之后  加上 login_user(username)

logout_user的应用
1.from flask-login import logout_user
2.逻辑判断
3.logout_user() #直接调用即可

flask-login提供用户登录 访问控制，没有登录的用户不能访问指定的页面，而用户直接跳转到登陆页面，这里需要用到@login_required装饰器并且告知flask-login 登录页面在哪里
    login = LoginManger(app)
    login.login_view = 'login'  #login  是url_for()里面的参数  指定登录视图在哪里

1.from flask-login import login_required
2.在视图函数上加上@login_required装饰器
eg：@app.route('/index')
    @login_required
    def index():
        ...

追溯登录前访问的页面，登录后 自动跳转到之前的需要访问的页面。flask-login强制跳转到登录页面时会在url中加入?next = '原页面地址',所以可用 flask  的request 来获取 url 中的参数
from flask import request
from werkzeug.urls import url_parse     #url解析函数

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ...
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        #url_parse(next_page).netloc != ''  url_parse().netloc是获取服务器地址,如果是站内跳转则在相对位置中 服务器地位为空  这样就提高了安全性
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # ...