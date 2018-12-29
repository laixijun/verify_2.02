from flask import json

from App.models import ExtraDbFile
from libs.error_code import success_desc, false_desc, ReturnDesc, ERRRecord
from libs.tools import RemoteSource
import re

from log.logging_file_console import logger


class FileAssert:
	def __init__(self):
		pass

	# 对比预期值和实际值
	def compareFile(self,compared_data,compare_data):
		if isinstance(compared_data,str):
			if compared_data==compare_data:
				return success_desc(desc="pass")
			elif compared_data!=compare_data:
				compare_data = compare_data.replace('\n', '').replace('\t', '').replace(' ', '')
				compared_data = compared_data.replace('\n', '').replace('\t', '').replace(' ', '')
				if compared_data == compare_data:
					return success_desc(desc="pass")
				elif compared_data != compare_data:
					return success_desc(desc="fail")

	#本地日志文件获取
	def getLocalSource(self,path):
		lyric = open(path, encoding="utf-8").read()
		logger.debug(lyric)
		return success_desc(desc=lyric)
	# 实际值的处理
	# ['6\n1234']
	def actulDeal(self,ip, username, passwd, cmd,regular,whereis):
		if whereis =="remote":
			actul_all=RemoteSource().ssh(ip=ip, username=username, passwd=passwd, cmd=cmd)
			logger.debug(actul_all)
		else:
			actul_all =self.getLocalSource(path=cmd)
		logger.debug(actul_all)
		if actul_all["code"]==1:
			actul_all=actul_all["desc"].encode("utf-8").decode()
			# actul_all=json.dumps(actul_all,encoding="utf-8")
			logger.debug(actul_all)
			reg=re.compile(regular,re.S)
			logger.debug(reg)
			reg_list=reg.findall(actul_all)
			logger.debug(reg_list)
			if len(reg_list)>=1:
				return success_desc(desc=reg_list)
			else:
				return ReturnDesc(desc=ERRRecord.REMOTEFILERECONTENT,code=ERRRecord.REMOTEFILERECONTENTNO).false_desc()
		elif actul_all["code"]==0:
			return actul_all


	def fileAssertMain(self,ip, username, passwd, cmd,regular,whereis,compare_data,uuid,project_name,project_version,id,infa_url,test_descript):
		from utils.functions import create_app
		app = create_app()
		ctx = app.app_context()
		ctx.push()
		item=self.actulDeal(ip, username, passwd, cmd,regular,whereis)
		logger.debug(item)
		if item["code"]==1:
			item=item["desc"][0]
			result=self.compareFile(compared_data=item,compare_data=compare_data)
			exe_result=json.dumps(success_desc(desc="db_pass"))
			if result["code"]==1:
				file_item=compare_data
				file_compare_result=result["desc"]
				file_actul_result=item
				ExtraDbFile.instert_file(uuid=uuid, project_name=project_name, project_version=project_version, id=id,
										 infa_url=infa_url, test_descript=test_descript, file_item=file_item,
									   file_compare_result=file_compare_result,file_actul_result=file_actul_result, exe_result=exe_result)
			elif result["code"] == 0:
				exe_result = json.dumps(result, ensure_ascii=False)
				ExtraDbFile.instert_db(uuid=uuid, project_name=project_name, project_version=project_version, id=id,
										 infa_url=infa_url, test_descript=test_descript,  exe_result=exe_result)
		elif item["code"]==0:
			exe_result=json.dumps(item,ensure_ascii=False)
			ExtraDbFile.instert_db(uuid=uuid, project_name=project_name, project_version=project_version, id=id,
										 infa_url=infa_url, test_descript=test_descript,  exe_result=exe_result)

if __name__ == "__main__":
	cmd = ['cat /tmp/zhy/a.log']  # 你要执行的命令列表
	username = "root"  # 用户名
	passwd = "123456"  # 密码
	# threads = []  # 多线程
	ip = "192.168.31.118"
	print("Begin......")
	regular="5(.*?)5"
	a=FileAssert().actulDeal(ip=ip, username=username, passwd=passwd, cmd=cmd,regular=regular)
	# actul_all = RemoteSource().ssh(ip=ip, username=username, passwd=passwd, cmd=cmd)
	# actul_all = RemoteSource().ssh(ip, username, passwd, cmd)
	# print(actul_all)
	print(a)