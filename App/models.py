from datetime import datetime
# 导入SQLAlchemy模块
from flask_sqlalchemy import SQLAlchemy
# 初始化db
db = SQLAlchemy()


#批量插入

class MoreDB:
	def __init__(self):
		self.db=db
		self.engine=db.get_engine()
	def insert(self,tablename,values=[]):
		# 主要是参考这部分如何批量插入
		with self.engine.connect() as connection:
			with connection.begin() as transaction:
				try:
					markers = ','.join('?' * len(values[0]))
					# 按段数拼成makers = '(?,?,?,?)'
					ins = 'INSERT INTO {tablename} (username,password) VALUES ({markers})'
					ins = ins.format(tablename=tablename.__tablename__, markers=markers)
					# 如果你的表已经存在了,widgets_table.name改成表名就行了.
					connection.execute(ins, values)
				except:
					transaction.rollback()
					raise
				else:
					transaction.commit()

class Grade(db.Model):
	"""班级模型"""
	g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	g_name = db.Column(db.String(20), unique=True)
	g_create_time = db.Column(db.DateTime, default=datetime.now)
	# 设置与班级 一对多的关联关系
	students = db.relationship('Student',backref= 'grade')
	# 自定义表名
	__tablename__ = 'grade'
	# 初始化字段 方便以后视图使用
	def __init__(self, name):
		self.g_name = name
	# 定义保存数据的方法 后面视图使用

	def save(self):
		db.session.add(self)
		db.session.commit()


class Student(db.Model):
     """学生模型"""
     s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
     s_name = db.Column(db.String(16), unique=True)
     s_sex = db.Column(db.Integer)
     # 设置与班级 一对多的关联关系
     grade_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

     __tablename__ = 'student'

     def __init__(self, s_name, s_sex,grade_id):
          self.s_name = s_name
          self.s_sex = s_sex
          self.grade_id =grade_id

     def save(self):
          db.session.add(self)
          db.session.commit()


class User(db.Model):
     """用户模型"""
     u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
     username = db.Column(db.String(16), unique=True)
     password = db.Column(db.String(250))
     u_create_time = db.Column(db.DateTime, default=datetime.now)
     # 用户和角色的一对多的关联关系
     role_id = db.Column(db.Integer, db.ForeignKey('role.r_id'))

     __tablename__ = 'user'

     def __init__(self,username,password):
          self.username = username
          self.password = password

     def save(self):
          db.session.add(self)
          db.session.commit()

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用例—回传结果—历史纪录表id
	name = db.Column(db.String(64))
	email = db.Column(db.String(64))
	pswd = db.Column(db.String(64))
	role_id = db.Column(db.Integer)  #用例id

	def __repr__(self):
		return "<User %r>" % self.name

	def __init__(self, username, email,password):
		self.name = username
		self.email = email
		self.pswd = password

	def save(self):
		db.session.add(self)
		db.session.commit()

	# def save(self):
	# 	db.session.add_all()
	# 	db.session.commit()


class NewReportTest(db.Model):
	__tablename__ = 'new_report_test'
	detail_report_history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用例—回传结果—历史纪录表id
	uuid = db.Column(db.String(50))
	project_name = db.Column(db.String(50))
	project_version = db.Column(db.String(50))
	id = db.Column(db.Integer)  #用例id
	infa_name = db.Column(db.String(100))  # 接口名称
	infa_method = db.Column(db.String(100))  # 接口方法
	infa_url = db.Column(db.String(500))  # url
	test_descript = db.Column(db.Text)  # 用例描述
	test_params = db.Column(db.Text)  # 用例参数
	except_descript = db.Column(db.Text)  # 预期结果
	example_json_params= db.Column(db.Text)  #json传参示例
	actul_descript = db.Column(db.Text)  # 实际结果
	exec_result = db.Column(db.Text)  #执行结果
	error_result = db.Column(db.Text)  #错误字段结果
	exec_time = db.Column(db.DateTime)  #测试执行时间


	def __init__(self, uuid, project_name,project_version,id,infa_name,infa_method,infa_url,test_descript,test_params,
	             except_descript,example_json_params,actul_descript,exec_result,error_result,exec_time):
		self.uuid = uuid
		self.project_name = project_name
		self.project_version = project_version
		self.id = id
		self.infa_name = infa_name
		self.infa_method = infa_method
		self.infa_url = infa_url
		self.test_descript = test_descript
		self.test_params = test_params
		self.except_descript = except_descript
		self.example_json_params = example_json_params
		self.actul_descript = actul_descript
		self.exec_result = exec_result
		self.error_result = error_result
		self.exec_time = exec_time
	# @staticmethod
	# def get(self,pro_uuid):
	# 	a=self.query.filter_by(uuid=pro_uuid).first()
	# 	b=(a.id, a.except_descript, a.exec_result, a.error_result, a.exec_time)
	# 	return b

	def save(self):
		db.session.add(self)
		db.session.commit()

class ExtraDbFile(db.Model):
	__tablename__ = 'extra_db_file'

	u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	uuid = db.Column(db.String(50))
	project_name = db.Column(db.String(50))
	project_version = db.Column(db.String(50))
	id = db.Column(db.Integer)  # 用例id
	infa_url = db.Column(db.String(500))  # url
	test_descript = db.Column(db.Text)  # 用例描述
	db_item = db.Column(db.Text)  # 数据库检查字段
	db_compare_result = db.Column(db.Text)  # 数据库检查字段结果
	db_actul_result = db.Column(db.Text)  # 数据库实际结果
	file_item = db.Column(db.Text)  # 文件检查内容
	file_compare_result = db.Column(db.Text)  # 文件检查结果
	file_actul_result = db.Column(db.Text)  # 数据库实际结果
	exe_result = db.Column(db.Text)  # 存在执行结果
	u_create_time = db.Column(db.DateTime, default=datetime.now)



	def __init__(self,uuid,project_name,project_version,infa_url,test_descript,db_item,db_compare_result,db_actul_result,file_item,file_compare_result,file_actul_result,exe_result):
		  self.uuid = uuid
		  self.project_name = project_name
		  self.project_version = project_version
		  self.id = id
		  self.infa_url = infa_url
		  self.test_descript = test_descript
		  self.db_item = db_item
		  self.db_compare_result = db_compare_result
		  self.db_actul_result = db_actul_result
		  self.file_item = file_item
		  self.file_compare_result = file_compare_result
		  self.file_actul_result = file_actul_result
		  self.exe_result = exe_result

	@staticmethod
	def instert_db(self,uuid,project_name,project_version,infa_url,test_descript,db_item,db_compare_result,db_actul_result,exe_result):
		ebf = ExtraDbFile(uuid,project_name,project_version,infa_url,test_descript,db_item,db_compare_result,db_actul_result,exe_result)
		db.session.add_all([ebf])
		db.session.commit()


	def save(self):
			db.session.add(self)
			db.session.commit()


class DBopreate:
	def __init__(self):
		pass
	def get(self,pro_uuid):
		result=db.session.query(NewReportTest).filter_by(uuid=pro_uuid).first() #values('id', 'except_descript', 'exec_result','error_result','exec_time')
		# a=[]
		print(result.except_descript)
		# for item in result:
		# 	print(item)
		# # return a




	def save(self):
		db.session.add(self)
		db.session.commit()


# 角色和权限的(多对多的)关联表
# r_p为关联表的表名

r_p = db.Table('r_p',
			   db.Column('role_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
			   db.Column('permission_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True))


class Role(db.Model):
     r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
     r_name = db.Column(db.String(10))
     # 用户和角色的一对多的关联关系
     users = db.relationship('User', backref='role')

     __tablename__ = 'role'

     def __init__(self,r_name):
          self.r_name = r_name

     def save(self):
          db.session.add(self)
          db.session.commit()


class Permission(db.Model):
     p_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
     p_name = db.Column(db.String(16), unique=True)
     p_er = db.Column(db.String(16), unique=True)
     # 角色和权限的多对多的关系
     roles = db.relationship('Role', secondary=r_p, backref=db.backref('permission', lazy=True))

     __tablename__ = 'permission'

     def __init__(self,p_name,p_er):
          self.p_name = p_name
          self.p_er = p_er

     def save(self):
          db.session.add(self)
          db.session.commit()
