from flask import json, Flask

from App.models import ExtraDbFile
from libs.error_code import ReturnDesc, ERRRecord
from libs.mysqlhelper import MysqlHelper


#变量类
from log.logging_file_console import logger


class Variate:
	pass


# 执行sql语句
# 查询到实际结果
# 校验结果
# 返回对比结果
class MysqlAssert:
	def __init__(self,USER=None,PASSWD=None,HOST=None,PORT=None,DB=None):
		if USER != None:
			self.USER =USER
		if PASSWD != None:
			self.PASSWD =PASSWD
		if HOST != None:
			self.HOST =HOST
		if PORT != None:
			self.PORT  =PORT
		if DB != None:
			self.DB =DB
	def getMysql(self):
		mySql = MysqlHelper(USER=self.USER, PASSWD=self.PASSWD, HOST=self.HOST, PORT=self.PORT, DB=self.DB)
		return mySql

	# 执行sql语句
	def exeSql(self,search_item,search_dt,search_key,search_value):
		try:
			if search_dt =="Null" or search_dt =="null" :
				sql=search_item
				result = self.getMysql().get_one(sql)
				logger.debug(result)
			else:
				sql="select "+search_item+" from "+search_dt+" where "+search_key+" = %s"
				params=(search_value)
				result=self.getMysql().get_one(sql,params)
			logger.debug(result)
			if result[0]:
				return ReturnDesc(desc=result[0]).success_desc()
			else:
				return ReturnDesc(desc=ERRRecord.REMOTEMYSQLCONTENT, code=ERRRecord.REMOTEMYSQLCONTENTNO).false_desc()

		except:
			return ReturnDesc(desc=ERRRecord.REMOTEMYSQL,code=ERRRecord.REMOTEMYSQLNO).false_desc()


	# 校验结果
	# 返回对比结果
	def compare(self,compared_data,compare_data):
		if isinstance(compared_data,str):
			if compared_data==compare_data:
				return self.success_desc(desc="pass")
			elif compared_data!=compare_data:
				return self.success_desc(desc="fail")
		elif not isinstance(compared_data,str):
			if not isinstance(compare_data,str):
				compare_data=str(compare_data)
			conversionData=self.data_type_conversion(dataed=compare_data, data=compared_data)
			if conversionData["code"]==1:
				conversionData=conversionData["desc"]
			else:
				return conversionData
			if compared_data==conversionData:
				return self.success_desc(desc="pass")
			elif compared_data!=conversionData:
				return self.success_desc(desc="fail")

	def mysqlAssertMain(self,search_item, search_dt, search_key, search_value,compare_data,uuid,project_name,project_version,id,infa_url,test_descript):
		# ctx = app.app_context()
		from utils.functions import create_app
		# app = Flask(__name__)
		app=create_app()
		ctx = app.app_context()
		ctx.push()
		item=self.exeSql(search_item, search_dt, search_key, search_value)
		logger.debug(item)
		if item["code"]==1:
			item=item["desc"]
			result=self.compare(compared_data=item,compare_data=compare_data)
			exe_result=json.dumps(self.success_desc(desc="db_pass"))
			if result["code"]==1:
				db_item=compare_data
				db_actul_result=item
				db_compare_result=result["desc"]
				# db_actul_result=compare_data
				ExtraDbFile.instert_db(uuid=uuid, project_name=project_name, project_version=project_version, id=id, infa_url=infa_url, test_descript=test_descript, db_item=db_item,
									   db_compare_result=db_compare_result,db_actul_result=db_actul_result, exe_result=exe_result)
			elif result["code"] == 0:
				exe_result = json.dumps(result, ensure_ascii=False)
				ExtraDbFile.instert_db(uuid=uuid, project_name=project_name, project_version=project_version,
								   id=id, infa_url=infa_url, test_descript=test_descript, exe_result=exe_result)
		elif item["code"]==0:
			exe_result=json.dumps(item,ensure_ascii=False)
			ExtraDbFile.instert_db(uuid=uuid, project_name=project_name, project_version=project_version,
								   id=id, infa_url=infa_url, test_descript=test_descript, exe_result=exe_result)

	def data_type_conversion(self, dataed, data):

		logger.debug(type(dataed))
		logger.debug(type(data))
		if isinstance(dataed, str):
			dataed = self.clear_string(dataed)
			if isinstance(data, int):
				dataed = int(dataed)
				return ReturnDesc(dataed).success_desc()
			elif isinstance(data, float):
				dataed = float(dataed)
				return ReturnDesc(dataed).success_desc()
			elif isinstance(data, list):
				if dataed[0] == '[':
					dataed = eval(dataed)
					logger.debug(dataed)
					return ReturnDesc(dataed).success_desc()
				else:
					return ReturnDesc(desc="预期参数结果错误" + dataed, code=701).false_desc()
			elif isinstance(data, tuple):
				if dataed[0] == '(':
					dataed = eval(dataed)
					return ReturnDesc(dataed).success_desc()
				else:
					return ReturnDesc(desc="预期参数结果错误" + dataed, code=701).false_desc()
			elif isinstance(data, dict):
				if dataed[0] == '{':
					dataed = eval(dataed)
					return ReturnDesc(dataed).success_desc()
				else:
					return ReturnDesc(desc="预期参数结果错误" + dataed, code=701).false_desc()

			else:
				return ReturnDesc(dataed).success_desc()
		else:
			return ReturnDesc(dataed).success_desc()

	def success_desc(self,desc):
		return {'code': 1, 'Msg': 'Suc', 'desc': desc}

	def false_desc(self,desc):
		return {'code': 0, 'Msg': 'Fail', 'desc': desc}


if __name__ =="__main__":
	MA=MysqlAssert("root","123456","127.0.0.1",3307,"Htai")

	"select project_version from new_report_test where uuid = '019c96ed-c3d2-4458-a49d-8d79e3b91bbe'"
	search_item="project_version"
	search_dt="new_report_test"
	search_dt = "null"
	search_key="uuid"
	search_value='"019c96ed-c3d2-4458-a49d-8d79e3b91bbe"'
	a=MA.exeSql(search_item,search_dt,search_key,search_value)
	# a = MA.exeSql()
	print(a)