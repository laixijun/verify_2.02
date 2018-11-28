import re

from libs.error_code import ReturnDesc
from log.logging_file_console import logger


class GETCompatibility:
	def __init__(self):
		pass
	def semicolon_colon_exists(self,test_params):
		if test_params[-1]==';':
			test_params=test_params[:-1]
		bracket=re.compile('\(-(.*?)-\)',re.S)
		params_name=[]
		params_value=[]
		test_params_list=test_params.split(';')
		logger.debug(test_params_list)
		if len(test_params_list)>1:
			for test_param_list in test_params_list:
				if '(-' in test_param_list:
					if '-):' in test_param_list:
						bracket_value = bracket.findall(test_param_list)
						params_name.append(bracket_value[0])
					if ':(-' in test_param_list:
						bracket_value=bracket.findall(test_param_list)
						params_value.append(bracket_value)
				else:
					test_param_lists=test_param_list.split(':')
					logger.debug(test_param_lists)
					if len(test_param_lists) > 1:
						params_name.append(test_param_lists[0])
						params_value.append(test_param_lists[1])
					else:
						return ReturnDesc("传入用例参数格式有误", 801).false_desc()
			return ReturnDesc([params_name,params_value]).success_desc()
		elif len(test_params_list)==1:
			test_params_list=test_params_list[0]
			if '(-' in test_params_list:
				if '-):' in test_params_list:
					bracket_value = bracket.findall(test_params_list)
					params_name.append(bracket_value[0])
				if ':(-' in test_params_list:
					bracket_value = bracket.findall(test_params_list)
					params_value.append(bracket_value)
			else:
				test_param_lists = test_params_list.split(':')
				logger.debug(test_param_lists)
				if len(test_param_lists) > 1:
					params_name.append(test_param_lists[0])
					params_value.append(test_param_lists[1])
				else:
					return ReturnDesc("传入用例参数格式有误", 801).false_desc()
			return ReturnDesc([params_name, params_value]).success_desc()
		else:
			return ReturnDesc("传入用例参数格式有误",801).false_desc()

	#获取（--）整个预期结果非键值类型
	def text_type(self,test_params):
		if '(-' == test_params[:2]:
			text_type_compile=re.compile('\(-(.*?)-\)')
			text_type_value=text_type_compile.findall(test_params)[0]
			return 	text_type_value
		else:
			return False

if __name__=='__main__':
	# test_params='from_om:internal;gps_type:(-bai:du-);lat:40.018597;lng:116.476326;\
	# 			mac:b4:30:52:5e:6d:61;model:HUAWEI-HUAWEI C8817E;name:先生;order_id:self.order_id;\
	# 			os:HUAWEI19,4.4.4;phone:13000000090;'
	a = 'fdasfawegrewg164651!@#@#$$$@#@-)'
	b=GETCompatibility().text_type(test_params=a)
	print(b)