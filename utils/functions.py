#utils中funtions.py文件中的类容,重要的配置
import os
# import redis

from flask import Flask
from App.user_views import user_blueprint

from App.models import db


def create_app():
    # 定义系统路径的变量
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	# 定义静态文件的路径
	static_dir = os.path.join(BASE_DIR, 'static')
	# 定义模板文件的路径
	templates_dir = os.path.join(BASE_DIR, 'templates')
	# 初始化app 和manage.py文件关联
	app = Flask(__name__,
				static_folder=static_dir,
				template_folder=templates_dir)
	# 注册蓝图
	app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
	# 配置mysql数据库
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/htai'
	#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/Htai'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	#配置json中文
	app.config['JSON_AS_ASCII'] = False
	app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
	# 设置session密钥
	app.config['SECRET_KEY'] = 'secret_key'
	# 设置连接的redis数据库 默认连接到本地6379
	app.config['SESSION_TYPE'] = 'redis'
	# 设置远程
	# App.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
	# 初始化db
	db.init_app(app=app)

	return app
