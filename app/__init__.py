from flask import  Flask
from flask_sqlalchemy  import  SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

# 扩展应用 必须先初始化
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate =Migrate(app,db)
login = LoginManager(app)
# flask-login 用户访问权限控制 如果没有登录 会强制跳转到指定的 视图 所以需要指定所需要跳转的视图
login.login_view = 'login'





from app import routes,models

