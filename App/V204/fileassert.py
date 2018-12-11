from flask import json

from App.models import ExtraDbFile
from libs.error_code import success_desc, false_desc, ReturnDesc, ERRRecord
from libs.tools import RemoteSource
import re

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
					return false_desc(desc="fail")
	# 实际值的处理
	# ['6\n1234']
	def actulDeal(self,ip, username, passwd, cmd,regular):
		actul_all=RemoteSource().ssh(ip=ip, username=username, passwd=passwd, cmd=cmd)
		if actul_all["code"]==1:
			actul_all=actul_all["desc"]
			reg=re.compile(regular,re.S)
			reg_list=reg.findall(actul_all)
			if len(reg_list)>=1:
				return success_desc(desc=reg_list)
			else:
				return ReturnDesc(desc=ERRRecord.REMOTEFILERECONTENT,code=ERRRecord.REMOTEFILERECONTENTNO).false_desc()
		elif actul_all["code"]==0:
			return actul_all

	def fileAssertMain(self,ip, username, passwd, cmd,regular,compare_data,uuid,project_name,project_version,id,infa_url,test_descript):
		item=self.actulDeal(self,ip, username, passwd, cmd,regular)
		if item["code"]==1:
			item=item["desc"][0]
			result=self.compareFile(compared_data=item,compare_data=compare_data)
			exe_result=json.dumps(self.success_desc(desc="db_pass"))
			if result["code"]==1:
				file_item=item
				file_compare_result=result["desc"]
				file_actul_result=compare_data
				ExtraDbFile.instert_file(uuid, project_name, project_version, id, infa_url, test_descript, file_item,
									   file_compare_result,file_actul_result, exe_result)
			elif result["code"] == 0:
				exe_result = json.dumps(result, ensure_ascii=False)
				ExtraDbFile.instert_db(uuid, project_name, project_version, id, infa_url, test_descript, exe_result)
		elif item["code"]==0:
			exe_result=json.dumps(item,ensure_ascii=False)
			ExtraDbFile.instert_db(uuid, project_name, project_version, id, infa_url, test_descript, exe_result)

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