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
#####################################################
用户注册 逻辑
1· 如同LoginForm 一样 先建立RegisterForm 并继承FlaskForm类
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

添加了两个自定义数据验证 validate_username 和 validate_email.  格式是 validate_<field_name>的函数，WTForms会自己加入到表单验证中

2·在视图中建立register视图  首先需要 from app.forms import RegisterForm
from app import db
from app.forms import RegistrationForm

# ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # 同样需要在 form.validate_on_submit()中写入数据库   自定义的validate_username 和 email 系统会自动验证
    if form.validate_on_submit():
    # 和在shell中的操作一样建立用户  db.session.add   db.session.commit
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


######################################################################
用户档案以及修改个人介绍

对于设计表单的页面 工作流程大致如下：
1·首先在Form.py 中建立相应的表单
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    #不要忘记相应的验证函数  每个表单需要单独添加 在form.validate_on_submit中才能应用
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValueError('该用户名已被注册！')

2·完成试图函数  @app.route()
首先 import 相应的表单Form
其次 在validate_on_submit()中 写入逻辑部分
最后 船只给模板 form=form
from app.forms import EditProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)



########################################################
修改用户档案还有问题存在
当用户名没有改变的情况下，提交也会显示该用户已存在

需要修改的地方有两处
1·forms.py 中
需要重载EditProfileForm是其接受一个变量orginal_name来存储当前用户的名称
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
#这一段用super对class进行了重载
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
后续判断是要判断修改的用户名是否等于初始用户名  等于则接受修改 否则查询数据库判断用户是否存在
2·需要修改试图函数
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # ...
    让试图函数接受当前用户名称