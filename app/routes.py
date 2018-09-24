from app import app
from flask import render_template,redirect,flash,url_for,request
from app.forms import LoginForm
from werkzeug.urls import url_parse
# 登录视图中需要验证用户 所以需要import User模型
from app.models import User
# 用户登录 登出 需要用到Flask_login的login_user 和 logout_user函数 和current_user属性来储存当前用户
from flask_login import login_user,logout_user,current_user,login_required

@app.route('/')
@app.route('/index')
# flask-login 访问权限判定 需要用到@login_required装饰器  放到其他装饰器下面，因为装饰器是从下向上的
@login_required
def index():
    return render_template('index.html',username = '左旭')

@app.route('/login',methods=['POST','GET'])
def login():
    # 先判断当前用户是否是已授权用户
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or form.password.data != user.password:
            flash('用户名不存在或密码错误')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        # 先判定是否从其他页面跳转到的login页面 ，以便登录后调回原来页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        # flash('登录用户名{},记住我 {}'.format(form.username.data,form.remember_me.data))
        return redirect(
            url_for('index')
        )
    return render_template('login.html',form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))