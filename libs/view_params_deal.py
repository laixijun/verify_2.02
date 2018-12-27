import re
from collections import Counter
from datetime import datetime
from uuid import uuid4

import requests
from flask import request, json

from App.V204.fileassert import FileAssert
from App.V204.mysqlAssert import MysqlAssert
from App.models import NewReportTest
from libs import mysqlhelper
from libs.compatibility import GETCompatibility
from libs.error_code import false, success, false_desc, success_desc, ReturnDesc
from libs.tools import threadingTimer
from log.logging_file_console import logger

class SoursDeal(object):
	def __init__(self):
		# self.tdb_deal=TestDBDeal()
		pass
	#url解析 单元测试通过

	def url_deal_v1(self,id,url_deal_mark1,method_requests,test_params,example_json_params_str):
		'''
		url内部的参数写变量名使用{}括住
		？之后的参数直接写在用例参数位置URL不体现
		:return:
		'''
		# url_deal_mark1_dict=self.tdb_deal.get_url(id=id,pro_uuid=pro_uuid)
		# if url_deal_mark1_dict['code']==1:
		# 	url_deal_mark1=url_deal_mark1_dict['desc'][0]
		# else:
		# 	return url_deal_mark1_dict

		# if "?" in url_deal_mark1:
		# 	index_params=url_deal_mark1.index("?")
		# 	url_deal_mark=url_deal_mark1[:index_params]
		# method_requests=self.url_method_deal(id=id,pro_uuid=pro_uuid)
		logger.debug(test_params)
		params_name_value_dict=self.test_params_deal(test_params=test_params)
		if params_name_value_dict['code']==1:
			params_name_value=params_name_value_dict['desc']
		else:
			return params_name_value_dict
		logger.debug(params_name_value)
		if params_name_value !=[]:
			params_name = params_name_value[0]
			params_value = params_name_value[1]
			params_name_value_dict_ok=Tools().list_to_dict(list_keys=params_name_value[0], list_values=params_name_value[1])
		url_deal_mark = url_deal_mark1.replace('\n', '').replace('\t', '').replace(' ', '')
		url_deal_mark_params=[]
		replace_str_dict={}
		variable_data=0
		if "{" in url_deal_mark:
			variable_data+=1
			re_com=re.compile("{(.*?)}")
			url_deal_mark_param_res=re_com.findall(url_deal_mark)
			logger.debug(url_deal_mark_param_res)
			for url_deal_mark_param_re in url_deal_mark_param_res:
				# params_value_value=params_name_value[1][params_name_value[0].index(url_deal_mark_param_re)]
				# url_deal_mark.replace(url_deal_mark_param_re,params_value_value)
				# params_name.remove(url_deal_mark_param_re)
				# params_value.remove(params_value_value)
				if url_deal_mark_param_re in params_name_value[0]:
					replace_str_dict[url_deal_mark_param_re]=params_name_value_dict_ok[url_deal_mark_param_re]
				else:
					return ReturnDesc("url给出的参数名与用例中的参数名不匹配,用例id为： "+str(id),806).false_desc()
			url_deal_mark_dict=Tools().replace_str(dict_data=replace_str_dict, str_data=url_deal_mark)
			if url_deal_mark_dict['code']==1:
				url_deal_mark=url_deal_mark_dict['desc']
			else:
				return url_deal_mark_dict
			logger.debug(url_deal_mark)
		if method_requests=='get'or method_requests=='GET':
			if params_name_value==[]:
				url_deal_mark_get_list=[url_deal_mark,[],'get']
				logger.debug(url_deal_mark_get_list)
				return ReturnDesc(url_deal_mark_get_list).success_desc()
			else:
			# 	re_com_first = re.compile("\?(.*?)=",re.S)
			# 	first_param=re_com_first.findall(url_deal_mark)
			# 	for first_param_singe in first_param:
			# 		url_deal_mark_params.append(first_param_singe)
			# 	re_com = re.compile("\&(.*?)=",re.S)
			# 	extra_params=re_com.findall(url_deal_mark)
			# 	for extra_param in extra_params:
			# 		url_deal_mark_params.append(extra_param)
			# 	list_params_flag=0
				if variable_data==1:
					params_value_name_get_data={}
					params_value_name_get_data_index=0
					for params_name_singe in params_name:
						if params_name_singe in url_deal_mark_param_res:
							params_value_name_get_data_index+=1
							continue
						params_value_name_get_data[params_name_singe]=params_value[params_value_name_get_data_index]
						params_value_name_get_data_index += 1
					logger.debug(params_value_name_get_data)
				else:
					params_value_name_get_data = self.test_params_deal_data(params_name, params_value)
					logger.debug(params_value_name_get_data)

			# 	for list_params in params_name_value[0]:
			# 		# if list_params in url_deal_mark_params:
			# 		# 	continue
			# 		list_params_value = params_name_value[1][params_name_value[0].index(list_params)]
			# 		params_value_name_get_data[list_params]=list_params_value
			return ReturnDesc([url_deal_mark,params_value_name_get_data,'get']).success_desc()
		elif method_requests == 'post'or method_requests == 'POST':
			if variable_data == 1:
				params_value_name_get_data = {}
				params_value_name_get_data_index = 0
				for params_name_singe in params_name:
					if params_name_singe in url_deal_mark_param_res:
						params_value_name_get_data_index += 1
						continue
					params_value_name_get_data[params_name_singe] = params_value[
						params_value_name_get_data_index]
					params_value_name_get_data_index += 1
			else:
				params_value_name_get_data = self.test_params_deal_data(params_name, params_value)
			post_list=[url_deal_mark,params_value_name_get_data,'post']
			return ReturnDesc(post_list).success_desc()
		elif method_requests == 'post_json' or method_requests == 'POST_JSON':
			if variable_data == 1:
				params_value_name_get_data = {}
				params_value_name_get_data_index = 0
				for params_name_singe in params_name:
					if params_name_singe in url_deal_mark_param_res:
						params_value_name_get_data_index += 1
						continue
					params_value_name_get_data[params_name_singe] = params_value[
						params_value_name_get_data_index]
					params_value_name_get_data_index += 1
			else:
				params_value_name_get_data = self.test_params_deal_data(params_name, params_value)
			# dict_params=Tools().list_to_dict(list_keys=params_name, list_values=params_value)
			data_requests_post_json_dict=self.example_json_params_data_deal_jsonpost(example_json_params_str=example_json_params_str, dict_params=params_value_name_get_data)
			# data_requests_post=self.test_params_deal_data(params_name,params_value)
			if data_requests_post_json_dict['code']==1:
				data_requests_post_json=data_requests_post_json_dict['desc']
			else:
				return data_requests_post_json_dict
			post_list=[url_deal_mark,data_requests_post_json,'post_json']
			return ReturnDesc(post_list).success_desc()
		else:
			return ReturnDesc("请求方式传参错误 id:"+str(id),809).false_desc()

	#接口方法解析   单元测试通过
	def url_method_deal(self,id,pro_uuid):
		url_method=self.tdb_deal.get_url_method(id=id,pro_uuid=pro_uuid)
		if url_method[0]=='post' or url_method[0]=='POST':
			return 'post'
		elif url_method[0]=='get' or url_method[0]=='GET':
			return 'get'
		elif url_method[0]=='post_json' or url_method[0]=='POST_JSON':
			return 'post_json'
	#用例传参解析  单元测试通过,
	def test_params_deal(self,test_params):
		# test_params= self.tdb_deal.get_test_params(id,pro_uuid)
		if test_params ==None or test_params=='':
			return ReturnDesc([]).success_desc()
		else:
			test_params_list_dict=GETCompatibility().semicolon_colon_exists(test_params)
			if test_params_list_dict['code']==1:
				test_params_list=test_params_list_dict['desc']
				logger.debug(test_params_list)
				return ReturnDesc(test_params_list).success_desc()
			else:
				return test_params_list_dict
	#预期结果解析
	def except_descript_deal(self,test_except,uuid,project_name,project_version,id,infa_url,test_descript):
		# test_except_dict=self.tdb_deal.get_except_descript(id=id,pro_uuid=pro_uuid)
		# if test_except_dict['code']==1:
		# 	test_except=test_except_dict['desc']
		# else:
		# 	return test_except_dict
		except_descript_deal_type_text=GETCompatibility().text_type(test_params=test_except)
		if except_descript_deal_type_text:
			return ReturnDesc(except_descript_deal_type_text).success_desc()
		else:
			except_descript_list_dict = GETCompatibility().semicolon_colon_exists(test_except)
			if except_descript_list_dict['code']==1:
				except_descript_list=except_descript_list_dict['desc']
			else:
				return except_descript_list_dict
			except_value_index = 0
			except_descript_deal_dict={}
			file_db_dict={}
			for except_name_single in except_descript_list[0]:
				if except_name_single[-3:]=="_db" or except_name_single[-5:]=="_file":
					except_name_single_list=except_name_single.split("___")
					logger.debug(except_name_single_list)
					file_db_dict[except_name_single]=except_name_single_list
					time=int(except_name_single_list[-2])
					compare_data = except_descript_list[1][except_value_index]
					except_value_index += 1
					if except_name_single_list[10] =="db":
						port=int(except_name_single_list[3])
						MA=MysqlAssert(USER=except_name_single_list[0],PASSWD=except_name_single_list[1],
									   HOST=except_name_single_list[2],PORT=port,DB=except_name_single_list[4])
						func=MA.mysqlAssertMain
						threadingTimer(time, func(except_name_single_list[5], except_name_single_list[6], except_name_single_list[7],
												   except_name_single_list[8],compare_data,uuid,project_name,project_version,id,infa_url,test_descript))
					elif except_name_single_list[10] =="file":
						func = FileAssert().fileAssertMain
						threadingTimer(time, func(
						except_name_single_list[0], except_name_single_list[1], except_name_single_list[2],
						except_name_single_list[3],except_name_single_list[4], compare_data, uuid, project_name, project_version, id, infa_url,
						test_descript))
					continue
				except_descript_deal_dict[except_name_single] = except_descript_list[1][except_value_index]
				except_value_index += 1
				logger.debug([except_descript_deal_dict,except_descript_list[0],file_db_dict])
			return ReturnDesc([except_descript_deal_dict,except_descript_list[0],file_db_dict]).success_desc()
	# 实际结果解析,返回格式需要时json
	# 如果字符串中键存在的个数为1个正常处理
	# 如果字符串中键存在的个数大于1时需要将所有值放到列表中并与键组成键值
	def actul_descript_deal(self,actul_descript_str,test_except):
		if test_except:
			except_names=test_except
		actul_descript_dic={}
		end_mark=[',',']',')','}']
		logger.debug(actul_descript_str)
		logger.debug(except_names)
		if isinstance(actul_descript_str,str):
			str_re = actul_descript_str.replace('\n', '').replace('\t', '').replace(' ', '')
			if str_re[1]=='"':
				for except_name in except_names:
					logger.debug(except_name)
					if str(str_re).count('"'+except_name+'"')>1:
						end_mark_re_v1_list_dict=self.end_mark_re_v1(except_name=except_name, str_data=str_re)
						if end_mark_re_v1_list_dict["code"]==0:
							return end_mark_re_v1_list_dict
						else:
							actul_descript_dic[except_name] = end_mark_re_v1_list_dict["desc"]
					elif str(str_re).count('"'+except_name+'"')==1:
						Double_quotation_mark_re=re.compile('"'+except_name+'":"(.*?)"')
						Double_quotation_mark_re_result=Double_quotation_mark_re.findall(str_re)
						Minato_ku_re = re.compile('"' + except_name + '":(.*?),')
						Minato_ku_re_result=Minato_ku_re.findall(str_re)
						if Double_quotation_mark_re_result !=[]:
							actul_descript_dic[except_name]=Double_quotation_mark_re_result[0]
						elif Minato_ku_re_result !=[]:
							actul_descript_dic[except_name] = Minato_ku_re_result[0]
						else:
							try:
								actul_descript_str = json.loads(actul_descript_str)
							except:
								actul_descript_str = json.dumps(actul_descript_str,ensure_ascii=False)
								actul_descript_str = json.loads(actul_descript_str)
							# end_mark_re_result=self.end_mark_re(except_name=except_name, str_data=str_re)
							grammar = '$..' + except_name
							logger.debug(actul_descript_str)
							logger.debug(grammar)
							end_mark_re_result = Tools().path(string_data=actul_descript_str, grammar=grammar)
							logger.debug(end_mark_re_result)
							# if end_mark_re_result['code']==0:
							# 	return end_mark_re_result
							# else:
							actul_descript_dic[except_name] = end_mark_re_result
			elif str_re[1]=="'":
				for except_name in except_names:
					if str(str_re).count("'"+except_name+"'") > 1:
						end_mark_re_v1_list_dict = self.end_mark_re_v1(except_name=except_name, str_data=str_re)
						if end_mark_re_v1_list_dict["code"] == 0:
							return end_mark_re_v1_list_dict
						else:
							actul_descript_dic[except_name] = end_mark_re_v1_list_dict["desc"]
					elif str(str_re).count("'"+except_name+"'") == 1:
						Double_quotation_mark_re=re.compile("'"+except_name+"':'(.*?)'")
						Double_quotation_mark_re_result=Double_quotation_mark_re.findall(str_re)
						Minato_ku_re = re.compile("'" + except_name + "':(.*?),")
						Minato_ku_re_result=Minato_ku_re.findall(str_re)
						if Double_quotation_mark_re_result !=[]:
							actul_descript_dic[except_name]=Double_quotation_mark_re_result[0]
						elif Minato_ku_re_result !=[]:
							actul_descript_dic[except_name] = Minato_ku_re_result[0]
						else:

							try:
								actul_descript_str = json.loads(actul_descript_str)
							except:
								actul_descript_str = json.dumps(actul_descript_str,ensure_ascii=False)
								actul_descript_str = json.loads(actul_descript_str)
							# end_mark_re_result = self.end_mark_re(except_name=except_name, str_data=str_re)
							grammar = '$..'+except_name
							end_mark_re_result = Tools().path(string_data=actul_descript_str, grammar=grammar)
							# # if end_mark_re_result['code']==0:
							# # 	return end_mark_re_result
							# # else:
							logger.debug(end_mark_re_result)
							actul_descript_dic[except_name] = end_mark_re_result
		logger.debug(actul_descript_dic)
		return actul_descript_dic
	#json传参示例解析
	def example_json_params_data_deal(self,id,list_params_name,dict_params):
		'''
		# list_params_name
		# dict_params
		# :param id:
		# :param list_params_name:
		# :param dict_params:
		# :return:
		'''
		example_json_params_str=self.tdb_deal.get_example_json_params(id)[0]
		# recom=re.compile('{.*?}',re.S)
		for list_param_name in list_params_name:
			example_json_params_str.replace(list_param_name,dict_params[list_param_name])
			print(example_json_params_str)
		example_json_params_json=json.loads(example_json_params_str)
		return example_json_params_json

	def example_json_params_data_deal_jsonpost(self,dict_params,example_json_params_str):
		'''
		# list_params_name
		# dict_params
		# :param id:
		# :param list_params_name:
		# :param dict_params:
		# :return:
		'''
		# example_json_params_str=self.tdb_deal.get_example_json_params(id=id,pro_uuid=pro_uuid)[0]
		logger.debug(example_json_params_str)
		example_json_params_str_dict=Tools().replace_str(dict_data=dict_params, str_data=example_json_params_str)
		if example_json_params_str_dict['code']==1:
			example_json_params_str=example_json_params_str_dict['desc']
		else:
			return example_json_params_str_dict
		example_json_params_json=json.loads(example_json_params_str)
		return ReturnDesc(example_json_params_json).success_desc()

	#如果字符串中键存在的个数为1个正常处理
	#如果字符串中键存在的个数大于1时需要将所有值放到列表中并与键组成键值
	def end_mark_re_v1(self,except_name,str_data):
		if isinstance(str_data,str):
			actul_descript_list=[]
			logger.debug(except_name)
			logger.debug(str_data)
			str_data=str(str_data)
			end_marks = [']', '\)', '}']
			result_string=[]
			str_data = str_data.replace('\n', '').replace('\t', '').replace(' ', '')
			if "'" in str_data:
				Double_quotation_mark_re_complile="'" + except_name + "':'(.*?)'"
				Double_quotation_mark_re_complile=Double_quotation_mark_re_complile.replace('\n', '').replace('\t', '').replace(' ', '')
				Double_quotation_mark_re = re.compile(Double_quotation_mark_re_complile)
				Double_quotation_mark_re_result = Double_quotation_mark_re.findall(str_data)
				Minato_ku_re_compile="'" + except_name + "':(.*?),"
				Minato_ku_re_compile=Minato_ku_re_compile.replace('\n', '').replace('\t', '').replace(' ', '')
				Minato_ku_re = re.compile(Minato_ku_re_compile)
				Minato_ku_re_result = Minato_ku_re.findall(str_data)
				if Double_quotation_mark_re_result != []:
					actul_descript_list += Double_quotation_mark_re_result
				if Minato_ku_re_result != []:
					for Minato_ku_re_result_item in Minato_ku_re_result:
						if "'" not in Minato_ku_re_result_item:
							actul_descript_list.append(Minato_ku_re_result_item)
				for end_mark in end_marks:
					# except_name + "':(.*?)" + end_mark, re.S
					compile_rule ="'"+except_name + "':(.*?)" + end_mark
					compile_rule = compile_rule.replace('\n', '').replace('\t', '').replace(' ', '')
					comp_re = re.compile(compile_rule, re.S)
					result_str = comp_re.findall(str_data)
					if len(result_str) !=0:
						# result_string.append(result_str[0])
						for result_strings in result_str:
							if "'" not in result_strings:
								result_string.append(result_strings)
			elif '"' in str_data:
				Double_quotation_mark_re_complile='"' + except_name + '":"(.*?)"'
				Double_quotation_mark_re_complile=Double_quotation_mark_re_complile.replace('\n', '').replace('\t', '').replace(' ', '')
				Double_quotation_mark_re = re.compile(Double_quotation_mark_re_complile)
				Double_quotation_mark_re_result = Double_quotation_mark_re.findall(str_data)
				Minato_ku_re_compile='"' + except_name + '":(.*?),'
				Minato_ku_re_compile=Minato_ku_re_compile.replace('\n', '').replace('\t', '').replace(' ', '')
				Minato_ku_re = re.compile(Minato_ku_re_compile)
				Minato_ku_re_result = Minato_ku_re.findall(str_data)
				if Double_quotation_mark_re_result != []:
					actul_descript_list += Double_quotation_mark_re_result
				if Minato_ku_re_result != []:
					for Minato_ku_re_result_item in Minato_ku_re_result:
						if '"' not in Minato_ku_re_result_item:
							actul_descript_list.append(Minato_ku_re_result_item)
				for end_mark in end_marks:
					compile_rule='"'+except_name + '":(.*?)' + end_mark
					compile_rule = compile_rule.replace('\n', '').replace('\t', '').replace(' ', '')
					comp_re = re.compile(compile_rule,re.S)
					result_str = comp_re.findall(str_data)
					logger.debug(result_str)
					if len(result_str) !=0:
						# result_string.append(result_str[0])
						for result_strings in result_str:
							if '"' not in result_strings:
								result_string.append(result_strings)
			# logger.debug(result_string)
			# if len(result_string)==3:
			# 	x=len(result_string[0])
			# 	y = len(result_string[1])
			# 	z = len(result_string[2])
			# 	logger.debug(x)
			# 	logger.debug(y)
			# 	logger.debug(z)
			# 	end_mark_str_num=(x if (x<y) else y) if ((x if (x<y) else y)<z) else z
			# 	if end_mark_str_num==x:
			# 		end_mark_str=result_string[0]
			# 	elif end_mark_str_num==y:
			# 		end_mark_str = result_string[1]
			# 	elif end_mark_str_num==z:
			# 		end_mark_str = result_string[2]
			# elif len(result_string)==2:
			# 	end_mark_str=result_string[0] if len(result_string[0])<len(result_string[1]) else result_string[1]
			# elif len(result_string)==1:
			# 	end_mark_str = result_string[0]
			# else:
			# 	return false_desc("未获取到值或解析失败")
			# double_comma_re=re.compile('"(.*?)"')
			# comma_re=re.compile("'(.*?)'")
			# if end_mark_str:
			# 	logger.debug(end_mark_str)
			# 	if "'" in end_mark_str:
			# 		end_mark_str=comma_re.findall(end_mark_str)[0]
			# 	elif '"' in end_mark_str:
			# 		end_mark_str=double_comma_re.findall(end_mark_str)[0]
			# 	logger.debug(end_mark_str)
			# 	return end_mark_str
			# else:
			# 	return false_desc("未获取到值或解析失败")
			logger.debug(result_string)
			logger.debug(actul_descript_list)
			result_string+=actul_descript_list
			return ReturnDesc(result_string).success_desc()
		else:
			return false_desc("处理字符串非json或string格式")

	def end_mark_re(self,except_name,str_data):
		if isinstance(str_data,str):
			#
			# str_data=str(str_data)
			# str_data=json.dumps(str_data)

			logger.debug(except_name)
			logger.debug(str_data)
			# str_data_str=str(str_data)
			# logger.debug(str_data_str)
			# str_data_json = json.dumps(str_data)
			# logger.debug(str_data_json)
			# data_resp_str_json=json.dumps(data_resp_str)
			# data_resp_str_str =str(data_resp_str)
			# if str_data==data_resp_str:
			# 	logger.debug('相等')
			# elif data_resp_str_json==str_data:
			# 	logger.debug('相等')
			# elif data_resp_str_str==str_data:
			# 	logger.debug('相等')
			# elif str_data_str==data_resp_str_str:
			# 	logger.debug('相等')
			# elif str_data_json==data_resp_str_json:
			# 	logger.debug('相等')
			# else:
			# 	logger.debug('不等')
			# logger.debug(type(str_data))
			str_data=str(str_data)
			end_marks = [']', '\)', '}']
			result_string=[]
			if "'" in str_data:
				for end_mark in end_marks:
					# except_name + "':(.*?)" + end_mark, re.S
					compile_rule =except_name + "':(.*?)" + end_mark
					compile_rule = compile_rule.replace('\n', '').replace('\t', '').replace(' ', '')
					comp_re = re.compile(compile_rule, re.S)
					result_str = comp_re.findall(str_data)
					if len(result_str) !=0:
						result_string.append(result_str[0])
			elif '"' in str_data:
				for end_mark in end_marks:
					compile_rule=except_name + '":(.*?)' + end_mark
					compile_rule = compile_rule.replace('\n', '').replace('\t', '').replace(' ', '')
					comp_re = re.compile(compile_rule,re.S)
					result_str = comp_re.findall(str_data)
					logger.debug(result_str)
					if len(result_str) !=0:
						result_string.append(result_str[0])
			logger.debug(result_string)
			if len(result_string)==3:
				x=len(result_string[0])
				y = len(result_string[1])
				z = len(result_string[2])
				logger.debug(x)
				logger.debug(y)
				logger.debug(z)
				end_mark_str_num=(x if (x<y) else y) if ((x if (x<y) else y)<z) else z
				if end_mark_str_num==x:
					end_mark_str=result_string[0]
				elif end_mark_str_num==y:
					end_mark_str = result_string[1]
				elif end_mark_str_num==z:
					end_mark_str = result_string[2]
			elif len(result_string)==2:
				end_mark_str=result_string[0] if len(result_string[0])<len(result_string[1]) else result_string[1]
			elif len(result_string)==1:
				end_mark_str = result_string[0]
			else:
				return false_desc("未获取到值或解析失败")
			double_comma_re=re.compile('"(.*?)"')
			comma_re=re.compile("'(.*?)'")
			if end_mark_str:
				logger.debug(end_mark_str)
				if "'" in end_mark_str:
					end_mark_str=comma_re.findall(end_mark_str)[0]
				elif '"' in end_mark_str:
					end_mark_str=double_comma_re.findall(end_mark_str)[0]
				logger.debug(end_mark_str)
				return end_mark_str
			else:
				return false_desc("未获取到值或解析失败")
		else:
			return false_desc("处理字符串非json或string格式")
	#解析postdata
	def test_params_deal_data(self,params_name,params_value):
		data_requests_post={}
		params_value_index=0
		for param_name in params_name:
			data_requests_post[param_name]=params_value[params_value_index]
			params_value_index+=1
		return data_requests_post

class SourceWay(object):

	def __init__(self,pro_uuid):
		# self.testdbdeal=TestDBDeal()
		self.soursdeal=SoursDeal()
		self.pro_uuid=pro_uuid
	'''
	def source_way(self,source='local'):
		if source=='local':
			if os.path.basename(path_test_report(pro='test'))=='infatest.xls':
				rows_num_test=self.testdbdeal.read_test_to_db(self.pro_uuid)
				if rows_num_test:
					for rows_num in rows_num_test:
						compare_result_list=self.compare_result(id=rows_num,pro_uuid=self.pro_uuid)
						logger.debug(compare_result_list)
						todb_reporttb_result=self.testdbdeal.todb_reporttb(id=rows_num,pro_uuid=self.pro_uuid)
						logger.debug(todb_reporttb_result)
					reporttb_to_excel_result=self.testdbdeal.reporttb_to_excel(pro_uuid=self.pro_uuid)
					if reporttb_to_excel_result['code']==1:
						copy_reporthistory=Result_db_history().copy_reporthistory_to_reporthistory(pro_uuid=self.pro_uuid)
						if copy_reporthistory['code']==1:
							reporttb_to_detail_history_result = Result_db_history().copy_reporthistory_to_detail_reporthistory()
							if reporttb_to_detail_history_result['code']==1:
								get_online_report_result=Tools().get_online_report(self.pro_uuid)
								if get_online_report_result['code']==1:
									# mysqlhelper.table_truncate(table_name='infatest')
									# mysqlhelper.table_truncate(table_name='infatestreport')
									return {'code':1,'msg':'suc'}
								else:
									return false_desc("数据返回临时表写入失败")
							else:
								return false_desc("详细报告历史记录写入失败")
						else:
							return false_desc("报告历史记录写入失败")
					else:
						return {'code': 0, 'msg': '写入Excel失败'}
				else:
					return {'code': 0, 'msg': '写入db失败'}
			else:
				return {'code': 0, 'msg': '上传文件不存在'}

		elif source=='online':
			rows_ids_test_dict=Tools().get_infatest_count(self.pro_uuid)
			logger.debug(rows_ids_test_dict)
			if rows_ids_test_dict['code']==1:
				for rows_num in rows_ids_test_dict['desc']:
					compare_result_list_dict = self.compare_result(id=rows_num,pro_uuid=self.pro_uuid)
					if compare_result_list_dict['code']==0:
						return compare_result_list_dict
					else:
						compare_result_list=compare_result_list_dict['desc']
					logger.debug(compare_result_list)
					todb_reporttb_result = self.testdbdeal.todb_reporttb(id=rows_num,pro_uuid=self.pro_uuid)
					logger.debug(todb_reporttb_result)
				reporttb_to_history_result=Result_db_history().copy_infatest_to_history(pro_uuid=self.pro_uuid)
				if reporttb_to_history_result['code']==1:
					reporttb_to_detail_history_result = Result_db_history().copy_reporthistory_to_detail_reporthistory()
					if reporttb_to_detail_history_result['code']==1:
						get_online_report_result = Tools().get_online_report(self.pro_uuid)
						if get_online_report_result['code']==1:
							# mysqlhelper.table_truncate(table_name='infatest')
							# mysqlhelper.table_truncate(table_name='infatestreport')
							return {'code':1,'msg':'suc'}
						else:
							return  get_online_report_result              #false_desc("数据返回临时表写入失败")
					else:
						return {'code': 0, 'msg': '写入detail—history表失败'}
				else:
					return {'code': 0, 'msg': '写入history表失败'}
			else:
				return rows_ids_test_dict
	'''
	# 生成实际测试结果，返回结果，并写入数据库
	def requests_test(self,id,pro_uuid):
		url_deal_dict=self.soursdeal.url_deal(id,pro_uuid)
		logger.debug(url_deal_dict)
		if url_deal_dict['code']==1:
			url_deal=url_deal_dict['desc']
		else:
			return url_deal_dict
		if url_deal[2]=='post':
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
			}
			try:
				actul_descript_resp=requests.post(url=url_deal[0],data=url_deal[1],headers=headers)
				if 200==actul_descript_resp.status_code:
					actul_descript_text=actul_descript_resp.text
				else:
					return ReturnDesc("访问url错误,用例id为："+ str(id),actul_descript_resp.status_code).false_desc()
			except:
				return ReturnDesc("url错误,用例id为："+ str(id),807 ).false_desc()
		elif url_deal[2]=='get':
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
			}
			logger.debug(url_deal[1])
			logger.debug(type(url_deal[1]))
			if url_deal[1]==[]:
				params = None
			else:
				params = url_deal[1]
			try:
				actul_descript_resp=requests.get(url=url_deal[0],headers=headers,params=params)
				if 200==actul_descript_resp.status_code:
					actul_descript_text=actul_descript_resp.text
				else:
					return ReturnDesc("访问url错误,用例id为："+ str(id),actul_descript_resp.status_code).false_desc()
			except:
				return ReturnDesc("url错误,用例id为："+ str(id),807 ).false_desc()
		elif url_deal[2]=='post_json':
			headers = {
				'Content-Type': 'application/json;charset=UTF-8',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
			           }
			try:
				actul_descript_resp = requests.post(url=url_deal[0], data=json.dumps(url_deal[1]),headers=headers)
				logger.debug(json.dumps(url_deal[1],ensure_ascii=False))
				if 200==actul_descript_resp.status_code:
					actul_descript_text=actul_descript_resp.text
				else:
					return ReturnDesc("访问url错误,用例id为："+ str(id),actul_descript_resp.status_code).false_desc()
				logger.debug(actul_descript_text)
			except:
				return ReturnDesc("url错误,用例id为："+ str(id),807 ).false_desc()
		self.testdbdeal.insert_actul_descript(actul_pt=actul_descript_text,id=id,pro_uuid=pro_uuid)
		actul_descript_compare_data=self.soursdeal.actul_descript_deal(id, actul_descript_text,pro_uuid=pro_uuid)
		return ReturnDesc(actul_descript_compare_data).success_desc()

	# 生成实际测试结果，返回结果，并写入数据库
	def requests_test_v1(self, id, url_deal_dict,test_except):
		# url_deal_dict = self.soursdeal.url_deal(id, pro_uuid)
		logger.debug(url_deal_dict)
		if url_deal_dict['code'] == 1:
			url_deal = url_deal_dict['desc']
		else:
			return url_deal_dict
		if url_deal[2] == 'post':
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
				# 'Content-Type':'mutipart/form-data'
			}
			try:
				actul_descript_resp = requests.post(url=url_deal[0], data=url_deal[1], headers=headers)
				if 200 == actul_descript_resp.status_code:
					actul_descript_text = actul_descript_resp.text
				else:
					return ReturnDesc("访问url错误,用例id为：" + str(id), actul_descript_resp.status_code).false_desc()
			except:
				return ReturnDesc("url错误,用例id为：" + str(id), 807).false_desc()
		elif url_deal[2] == 'get':
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
			}
			logger.debug(url_deal[1])
			logger.debug(type(url_deal[1]))
			if url_deal[1] == []:
				params = None
			else:
				params = url_deal[1]
			try:
				actul_descript_resp = requests.get(url=url_deal[0], headers=headers, params=params)
				if 200 == actul_descript_resp.status_code:
					actul_descript_text = actul_descript_resp.text
				else:
					return ReturnDesc("访问url错误,用例id为：" + str(id), actul_descript_resp.status_code).false_desc()
			except:
				return ReturnDesc("url错误,用例id为：" + str(id), 807).false_desc()
		elif url_deal[2] == 'post_json':
			headers = {
				'Content-Type': 'application/json;charset=UTF-8',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
			}
			try:
				actul_descript_resp = requests.post(url=url_deal[0], data=json.dumps(url_deal[1],ensure_ascii=False).encode(), headers=headers)
				logger.debug(json.dumps(url_deal[1], ensure_ascii=False))
				if 200 == actul_descript_resp.status_code:
					actul_descript_text = actul_descript_resp.text
				else:
					return ReturnDesc("访问url错误,用例id为：" + str(id), actul_descript_resp.status_code).false_desc()
				logger.debug(actul_descript_text)
			except:
				return ReturnDesc("url错误,用例id为：" + str(id), 807).false_desc()
		# self.testdbdeal.insert_actul_descript(actul_pt=actul_descript_text, id=id, pro_uuid=pro_uuid)
		actul_descript_compare_data = self.soursdeal.actul_descript_deal(actul_descript_text, test_except=test_except)
		logger.debug(actul_descript_text)
		logger.debug(actul_descript_compare_data)
		return ReturnDesc(actul_descript_compare_data).success_desc()


	# 生成实际测试结果，返回结果，并写入数据库
	# 对比实际结果与预期结果，写入数据库
	def compare_result(self,actul_descript_compare_data_dict,test_except):
		# actul_descript_compare_data_dict=self.requests_test(id,pro_uuid)
		if actul_descript_compare_data_dict['code']==1:
			actul_descript_compare_data=actul_descript_compare_data_dict['desc']
			logger.debug(actul_descript_compare_data)
			if test_except:
				except_descript_compare_data=test_except
			else:
				return false_desc("预期结果解析错误")
			logger.debug(except_descript_compare_data)
			# print(actul_descript_compare_data,except_descript_compare_data)
			compare_result_list=[]
			compare_flag=0
			compare_flag_flag = 0
			try:
				for except_descript_compare_data_singe in except_descript_compare_data[1]:
					# except_descript_compare_data_singe=Tools().clear_string(except_descript_compare_data_singe)
					except_descript_compare_data_except_descript_compare_data_singe=Tools().clear_string(except_descript_compare_data[0][except_descript_compare_data_singe])
					if not isinstance(actul_descript_compare_data[except_descript_compare_data_singe],list):
						actul_descript_compare_data_except_descript_compare_data_singe=Tools().clear_string(str(actul_descript_compare_data[except_descript_compare_data_singe]))
					# logger.debug(except_descript_compare_data_except_descript_compare_data_singe)
					# logger.debug(actul_descript_compare_data_except_descript_compare_data_singe)
					# logger.debug(type(except_descript_compare_data_except_descript_compare_data_singe))
					# logger.debug(type(actul_descript_compare_data_except_descript_compare_data_singe))
						except_descript_compare_data_except_descript_compare_data_singe_dict=Tools().data_type_conversion(dataed=except_descript_compare_data_except_descript_compare_data_singe,
						                             data=actul_descript_compare_data_except_descript_compare_data_singe)
						if except_descript_compare_data_except_descript_compare_data_singe_dict['code']==1:
							except_descript_compare_data_except_descript_compare_data_singe=except_descript_compare_data_except_descript_compare_data_singe_dict['desc']
						else:
							return except_descript_compare_data_except_descript_compare_data_singe_dict
					# logger.debug(except_descript_compare_data_except_descript_compare_data_singe)
					# logger.debug(actul_descript_compare_data_except_descript_compare_data_singe)
					# logger.debug(type(except_descript_compare_data_except_descript_compare_data_singe))
					# logger.debug(type(actul_descript_compare_data_except_descript_compare_data_singe))
					# if not isinstance(actul_descript_compare_data_except_descript_compare_data_singe,list):
						if actul_descript_compare_data_except_descript_compare_data_singe == except_descript_compare_data_except_descript_compare_data_singe:
							exec_result={'code':1,'msg':'suc','pro':except_descript_compare_data_singe}
						elif actul_descript_compare_data_except_descript_compare_data_singe != except_descript_compare_data_except_descript_compare_data_singe:
							exec_result = {'code': 0, 'msg': 'fail','pro':except_descript_compare_data_singe}
					else:
						logger.debug(except_descript_compare_data_except_descript_compare_data_singe)
						logger.debug(actul_descript_compare_data[except_descript_compare_data_singe])
						except_descript_compare_data_except_descript_compare_data_singe_dict = Tools().data_type_conversion(
							dataed=except_descript_compare_data_except_descript_compare_data_singe,
							data=actul_descript_compare_data[except_descript_compare_data_singe])
						logger.debug(except_descript_compare_data_except_descript_compare_data_singe_dict)
						if except_descript_compare_data_except_descript_compare_data_singe_dict[
							'code'] == 1:
							except_descript_compare_data_except_descript_compare_data_singe = \
								except_descript_compare_data_except_descript_compare_data_singe_dict['desc']
						else:
							return except_descript_compare_data_except_descript_compare_data_singe_dict
						logger.debug(except_descript_compare_data_except_descript_compare_data_singe)
						logger.debug(type(except_descript_compare_data_except_descript_compare_data_singe))
						logger.debug(actul_descript_compare_data[except_descript_compare_data_singe])
						logger.debug(type(actul_descript_compare_data[except_descript_compare_data_singe]))
						if len(actul_descript_compare_data[except_descript_compare_data_singe]) != len(except_descript_compare_data_except_descript_compare_data_singe):
							compare_flag += 1
						else:
							actul_descript_compare_data_list=[]
							except_descript_compare_data_list=[]
							for actul_descript_compare_data_except_descript_compare_data_singe_item in actul_descript_compare_data[except_descript_compare_data_singe]:

								actul_descript_compare_data_except_descript_compare_data_singe_item = Tools().clear_string(
									str(actul_descript_compare_data_except_descript_compare_data_singe_item))
								actul_descript_compare_data_list.append(actul_descript_compare_data_except_descript_compare_data_singe_item)
							for except_descript_compare_data_except_descript_compare_data_singe_item in except_descript_compare_data_except_descript_compare_data_singe:
								except_descript_compare_data_except_descript_compare_data_singe_item = Tools().clear_string(
									str(except_descript_compare_data_except_descript_compare_data_singe_item))
								except_descript_compare_data_except_descript_compare_data_singe_dict = Tools().data_type_conversion(
									dataed=except_descript_compare_data_except_descript_compare_data_singe_item,
									data=actul_descript_compare_data_except_descript_compare_data_singe_item)
								if except_descript_compare_data_except_descript_compare_data_singe_dict[
									'code'] == 1:
									except_descript_compare_data_except_descript_compare_data_singe_item = \
									except_descript_compare_data_except_descript_compare_data_singe_dict['desc']
								else:
									return except_descript_compare_data_except_descript_compare_data_singe_dict
								except_descript_compare_data_list.append(except_descript_compare_data_except_descript_compare_data_singe_item)
							actul_descript_compare_data_list_counter=Counter(actul_descript_compare_data_list)
							except_descript_compare_data_list_counter=Counter(except_descript_compare_data_list)
							for actul_descript_compare_data_list_item in actul_descript_compare_data_list:
								# for except_descript_compare_data_list_item in except_descript_compare_data_list:
								if actul_descript_compare_data_list_counter[actul_descript_compare_data_list_item]!=\
										except_descript_compare_data_list_counter[actul_descript_compare_data_list_item]:
									# if actul_descript_compare_data_except_descript_compare_data_singe_item == except_descript_compare_data_except_descript_compare_data_singe_item:
										compare_flag_flag+=1
						if compare_flag ==0 and compare_flag_flag==0:
							exec_result = {'code': 1, 'msg': 'suc', 'pro': except_descript_compare_data_singe}
						else:
							exec_result = {'code': 0, 'msg': 'fail', 'pro': except_descript_compare_data_singe}
						compare_flag=0
						compare_flag_flag = 0
					compare_result_list.append(exec_result)
				# self.testdbdeal.insert_exec_result(exec_result=json.dumps(compare_result_list,ensure_ascii=False), id=id,pro_uuid=pro_uuid)
				# self.testdbdeal.insert_exec_time(id=id,pro_uuid=pro_uuid)
				compare_re=[]
				compare_re.append(compare_result_list)
				compare_re.append(datetime.now())
				logger.debug(compare_result_list)
				return ReturnDesc(compare_re).success_desc()
			except KeyError as e:
				return false_desc("预期结果与实际结果key错误 : " + str(e))
		else:
			return actul_descript_compare_data_dict

class TestParamsDeal:
	def __init__(self):
		self.deal_db=mysqlhelper
	#接收参数，将参数保存到目录表，用例表，用例历史表，
	def testparamsdeal(self):
		data=request.json
		# test_param_list_to_db_tuple_tuple=[]
		logger.debug(data)
		json_params_assert_result=Tools().json_params_assert(json_contents=data)
		if json_params_assert_result['code']!=1:
			return json_params_assert_result
		else:
			# get_project_info_result=self.get_project_info(json_data=data)
			pro_uuid=json.dumps(uuid4())
			if pro_uuid:
				test_param_list_to_db_list=[]
				return_test_param_list_to_db_list = []
				return_test_param_list_to_db_dict = {}
				return_test_param_list_to_db_dict_dict={}
				for test_param_list in data["test_param"]:
					#解析参数返回解析URL返回
					logger.debug(test_param_list["test_params"])
					url_deal_dict=SoursDeal().url_deal_v1(id=test_param_list["id"], url_deal_mark1=test_param_list["URL"],
					                                              method_requests=test_param_list["method"],
					                                              test_params=test_param_list["test_params"],
					                                              example_json_params_str=test_param_list["example_json_params"])
					logger.debug(url_deal_dict)
					#获取预期结果
					except_descript_deal_dict=SoursDeal().except_descript_deal(test_except=test_param_list["except_descript"],
																			   uuid=pro_uuid,project_name=data["project_name"],project_version=data['project_version'],
																			   id=test_param_list["id"],infa_url=test_param_list["URL"],test_descript=test_param_list["test_descript"])
					if except_descript_deal_dict['code'] == 1:
						except_descript_deal_dict = except_descript_deal_dict['desc']
					else:
						return except_descript_deal_dict
					#返回实际测试结果，字典类型
					actul_descript_compare_data_dict=SourceWay(pro_uuid).requests_test_v1(id=test_param_list["id"], url_deal_dict=url_deal_dict,test_except=except_descript_deal_dict[0])
					#返回实际结果和预期结果的对比结果0，和对比执行时间1  列表类型
					logger.debug(actul_descript_compare_data_dict)
					get_online_report=SourceWay(pro_uuid).compare_result(actul_descript_compare_data_dict=actul_descript_compare_data_dict, test_except=except_descript_deal_dict)
					logger.debug(get_online_report)
					if get_online_report["code"]==1:
						get_online_report=get_online_report["desc"]
					else:
						return get_online_report
					#返回列表类型，错误字段列表0，执行结果1
					get_online_report_result=Tools().get_online_report_v1(get_online_report=get_online_report)
					logger.debug(get_online_report_result)
					if get_online_report_result["code"]==1:
						get_online_report_result=get_online_report_result["desc"]
					else:
						return get_online_report_result
					test_param_list_to_db_list.append(pro_uuid)
					test_param_list_to_db_list.append(data["project_name"])
					test_param_list_to_db_list.append(data['project_version'])
					test_param_list_to_db_list.append(test_param_list["id"])
					test_param_list_to_db_list.append(test_param_list["infa_name"])
					test_param_list_to_db_list.append(test_param_list["method"])
					test_param_list_to_db_list.append(test_param_list["URL"])
					test_param_list_to_db_list.append(test_param_list["test_descript"])
					test_param_list_to_db_list.append(test_param_list["test_params"])
					test_param_list_to_db_list.append(test_param_list["except_descript"])
					test_param_list_to_db_list.append(json.dumps(test_param_list["example_json_params"],ensure_ascii=False))
					test_param_list_to_db_list.append(json.dumps(actul_descript_compare_data_dict,ensure_ascii=False))
					test_param_list_to_db_list.append(get_online_report_result[1])
					test_param_list_to_db_list.append(json.dumps(get_online_report_result[0], ensure_ascii=False))
					test_param_list_to_db_list.append(get_online_report[1])
					# test_param_list_to_db_tuple=tuple(test_param_list_to_db_list)
					# test_param_list_to_db_tuple_tuple.append(test_param_list_to_db_tuple)
					logger.debug(test_param_list_to_db_list)
					Tools().json_to_db_test_report_v1(json_contents=test_param_list_to_db_list)
					logger.debug(test_param_list_to_db_list)
					test_param_list_to_db_list=[]
					return_test_param_list_to_db_dict['id'] = test_param_list["id"]
					return_test_param_list_to_db_dict['exec_result']=get_online_report_result[1]
					return_test_param_list_to_db_dict['error_result'] = get_online_report_result[0]
					return_test_param_list_to_db_dict['exec_time'] = get_online_report[1].strftime('%Y-%m-%d %H:%M:%S')
					return_test_param_list_to_db_list.append(return_test_param_list_to_db_dict)
					return_test_param_list_to_db_dict={}
				return_test_param_list_to_db_dict_dict['code'] = 1
				return_test_param_list_to_db_dict_dict['msg'] = "suc"
				return_test_param_list_to_db_dict_dict['uuid']=pro_uuid
				return_test_param_list_to_db_dict_dict['project_name'] = data["project_name"]
				return_test_param_list_to_db_dict_dict['project_version'] = data['project_version']
				return_test_param_list_to_db_dict_dict['result'] = return_test_param_list_to_db_list
				# test_param_list_to_db_tuple=tuple(test_param_list_to_db_tuple_tuple)
				# inserttodb_test_report=Tools().json_to_db_test_report(json_contents=test_param_list_to_db_tuple)
				logger.debug(return_test_param_list_to_db_dict_dict)
				return ReturnDesc(return_test_param_list_to_db_dict_dict).success_desc()
				# if inserttodb_test_report['code']==1:
				# 	# test_param_list_to_db_list=list(test_param_list_to_db_tuple)
				# 	# test_param_list_to_db_tuple=tuple(test_param_list_to_db_list)
				# 	# logger.debug(test_param_list_to_db_tuple)
				# 	# inserttodb_test_report_history = Tools().json_to_db_test_report_history(
				# 	# 	json_contents=test_param_list_to_db_tuple)
				# 	# logger.debug(inserttodb_test_report_history)
				# 	# if inserttodb_test_report_history['code']==1:
				# 	# 	test_param_list_to_db_list = []
				# 	# else:
				# 	# 	return inserttodb_test_report
				# 	return ReturnDesc(return_test_param_list_to_db_dict_dict).success_desc()
				# else:
				# 	return false()




	#获取项目名称和项目版本，创建UUID,将获取信息保存到目录表中
	def get_project_info(self,json_data):
		# project_info = []
		json_uuid = json.dumps(uuid4())
		# project_info.append(json_uuid)
		# project_info.append(json_data['project_name'])
		# project_info.append(json_data['project_version'])
		# project_info.append(datetime.now())
		# project_info_tuple=tuple(project_info)
		# get_project_info_result=Tools().json_to_db_reportuuid(uuid_db_param=project_info_tuple)
		# logger.debug(get_project_info_result['code'])
		if json_uuid:
			return {'code': 1, 'msg': 'suc','uuid_reportuuid':json_uuid}
		else:
			return false()

	#获取项目名称和版本信息，存入目录表
	def get_project_info_upload_file(self):
		dict_data=request.form.to_dict()
		logger.debug(dict_data)
		logger.debug(type(dict_data))
		project_info = []
		json_uuid = str(uuid4())
		project_info.append(json_uuid)
		project_info.append(dict_data['project_name'])
		project_info.append(dict_data['project_version'])
		project_info.append(datetime.now())
		project_info_tuple = tuple(project_info)
		get_project_info_result = Tools().json_to_db_reportuuid(uuid_db_param=project_info_tuple)
		logger.debug(get_project_info_result['code'])
		if get_project_info_result['code'] == 1:
			return {'code': 1, 'msg': 'suc', 'uuid_reportuuid': json_uuid}
		else:
			return false()

class Result_db_history:
	def __init__(self):
		pass

	def copy_infatest_to_history(self,pro_uuid):
		sql='select actul_descript,exec_result,exec_time,id from infatest where uuid=%s'
		params=(pro_uuid,)
		infatest_date_tuples=mysqlhelper.get_all(sql=sql,params=params)
		sql_history='update testreporthistory set actul_descript=%s,detail_exec_result=%s,exec_time=%s where id=%s and uuid=%s'
		# pro_uuid=Tools().search_new_uuid()
		logger.debug(infatest_date_tuples)
		for infatest_date_tuple in infatest_date_tuples:
			logger.debug(infatest_date_tuple)
			infatest_date_list=list(infatest_date_tuple)
			infatest_date_list.append(pro_uuid)
			infatest_date_tuple=tuple(infatest_date_list)
			logger.debug(infatest_date_tuple)
			mysqlhelper.update(sql=sql_history,params=infatest_date_tuple)
		return success()

	#将临时详细报告表中的数据，复制到历史记录表
	def copy_reporthistory_to_detail_reporthistory(self):
		reportuuid_sql='select project_name,project_version from reportuuid order by report_uuid_id desc limit 1 '
		reportuuid_data_tuples=mysqlhelper.get_one(reportuuid_sql)
		infatestreport_sql ='select report_id,id,uuid,' \
		                         'infa_name,infa_method,infa_url,test_descript,test_params,except_descript,example_json_params,' \
		                         'actul_descript,detail_exec_result,exec_time from infatestreport'
		infatestreport_data_tuples = mysqlhelper.get_all(infatestreport_sql)
		detail_reporthistory_sql='insert into detailreporthistory(project_name,project_version,report_id,id,uuid,' \
		                         'infa_name,infa_method,infa_url,test_descript,test_params,except_descript,example_json_params,' \
		                         'actul_descript,detail_exec_result,exec_time)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		for infatestreport_data_tuple in infatestreport_data_tuples:
			reportuuid_data_list=list(reportuuid_data_tuples)
			infatestreport_data_list=list(infatestreport_data_tuple)
			reportuuid_data_list+=infatestreport_data_list
			reportuuid_data_tuple=tuple(reportuuid_data_list)
			mysqlhelper.insert(sql=detail_reporthistory_sql,params=reportuuid_data_tuple)

		return success()

		# 将临时报告表中的数据，复制到历史记录表
	def copy_reporthistory_to_reporthistory(self,pro_uuid):
		reportuuid_sql = 'select project_name,project_version from reportuuid order by report_uuid_id desc limit 1 '
		reportuuid_data_tuples = mysqlhelper.get_one(reportuuid_sql)
		infatest_sql = 'select id,uuid,' \
		                           'infa_name,infa_method,infa_url,test_descript,test_params,except_descript,example_json_params,' \
		                           'actul_descript,exec_result,exec_time from infatest where uuid=%s'
		params=(pro_uuid,)
		infatest_data_tuples = mysqlhelper.get_all(infatest_sql,params=params)
		detail_reporthistory_sql = 'insert into testreporthistory(project_name,project_version,id,uuid,' \
		                           'infa_name,infa_method,infa_url,test_descript,test_params,except_descript,example_json_params,' \
		                           'actul_descript,detail_exec_result,exec_time)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		for infatest_data_tuple in infatest_data_tuples:
			reportuuid_data_list = list(reportuuid_data_tuples)
			infatest_data_list = list(infatest_data_tuple)
			reportuuid_data_list += infatest_data_list
			reportuuid_data_tuple = tuple(reportuuid_data_list)
			mysqlhelper.insert(sql=detail_reporthistory_sql, params=reportuuid_data_tuple)

		return success()

class Tools:
	def __init__(self):
		pass

	def json_params_assert(self,json_contents):
		if json_contents is None:
			return  ReturnDesc('传入参数格式不正确或未传入参数',802).false_desc()   #false_desc('传入参数格式不正确或未传入参数')
		if json_contents["test_param"]==[] or json_contents["test_param"]=='' or not isinstance(json_contents["test_param"],list):
			return ReturnDesc('参数无用例列表或用例列表格式不正确', 803).false_desc()#false_desc('传入参数无用例或用例格式不正确')
		params_error_list=[]
		params_error_list_id=[]
		params_error_list_id_err = []
		logger.debug(json_contents["test_param"])
		for item_test in json_contents["test_param"]:
			if item_test['method']!='' and (item_test['method']=='post'or item_test['method']=='POST'):
				if item_test['id']=='' or not isinstance(item_test['id'],int) or item_test['method']=='' or item_test['URL']=='' or item_test['test_params']=='' \
					or item_test['except_descript']=='':
					params_error_list.append(item_test['id'])
			elif item_test['method']!='' and (item_test['method']=='get'or item_test['method']=='GET'):
				if item_test['id']=='' or not isinstance(item_test['id'],int) or item_test['method']=='' or item_test['URL']=='' \
					or item_test['except_descript']=='':
					params_error_list.append(item_test['id'])
			elif item_test['method'] != '' and (item_test['method']=='post_json'or item_test['method']=='POST_JSON'):
				if item_test['id'] == '' or not isinstance(item_test['id'], int) or item_test['method'] == '' or \
						item_test['URL'] == '' \
						or item_test['except_descript'] == ''or item_test["example_json_params"]== '':
					params_error_list.append(item_test['id'])
			elif item_test['method'] == '':
				params_error_list.append(item_test['id'])
			if item_test['id'] not in params_error_list_id:
				params_error_list_id.append(item_test['id'])
			else:
				params_error_list_id_err.append(item_test['id'])
		if params_error_list_id_err != []:
			return ReturnDesc('列表中的用例id重复 '+str(params_error_list_id_err),805).false_desc()
		if params_error_list !=[]:
			return ReturnDesc('列表中的用例，必填项未正确填写 '+str(params_error_list),804).false_desc() #false_desc('列表中的用例，必填项未正确填写'+str(params_error_list))
		return success()
	#插入infatest表
	def json_to_db_test_report(self,json_contents):
		try:
			sql = 'insert into new_report_test(uuid,project_name,project_version,id,infa_name,infa_method,infa_url,test_descript,test_params,' \
			      'except_descript,example_json_params,actul_descript,exec_result,error_result,exec_time) values' \
			      '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			mysqlhelper.insert(sql=sql, params=json_contents)
			return {'code':1,'msg':'suc'}
		except:
			return false_desc("数据库导入失败")

	def json_to_db_test_report_v1(self,json_contents):
		new_report_test=NewReportTest(json_contents[0],json_contents[1],json_contents[2],json_contents[3],json_contents[4],
		                              json_contents[5],json_contents[6],json_contents[7],json_contents[8],json_contents[9],
		                              json_contents[10],json_contents[11],json_contents[12],json_contents[13],json_contents[14],)

		new_report_test.save()

	def json_to_db_test_report_history(self,json_contents):
		sql = 'insert into testreporthistory(id,uuid,infa_name,infa_method,infa_url,test_descript,test_params,' \
		      'except_descript,example_json_params,project_name,project_version) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		mysqlhelper.insert(sql=sql, params=json_contents)
		return {'code':1,'msg':'suc'}

	def json_to_db_test_report_history_info(self,json_contents_info):
		sql = 'insert into testreporthistory(uuid,project_name,project_version) values(%s,%s,%s)'
		mysqlhelper.insert(sql=sql, params=json_contents_info)
		return {'code':1,'msg':'suc'}

	def update_json_to_db_test_report_history(self,json_contents_list,pro_uuid,test_id):
		sql = 'update testreporthistory set id=%s,infa_name=%s,infa_method=%s,infa_url=%s,test_descript=%s,test_params=%s,' \
		      'except_descript=%s,example_json_params=%s where pro_uuid=%s and test_id=%s'
		json_contents_list.append(pro_uuid)
		json_contents_list.append(test_id)
		json_contents=tuple(json_contents_list)
		mysqlhelper.insert(sql=sql, params=json_contents)
		return {'code':1,'msg':'suc'}

	def update_json_to_db_test_report_history_actul_descript(self,json_contents_list,pro_uuid,test_id):
		sql = 'update testreporthistory set id=%s,infa_name=%s,infa_method=%s,infa_url=%s,test_descript=%s,test_params=%s,' \
		      'except_descript=%s,example_json_params=%s where pro_uuid=%s and test_id=%s'
		json_contents_list.append(pro_uuid)
		json_contents_list.append(test_id)
		json_contents=tuple(json_contents_list)
		mysqlhelper.insert(sql=sql, params=json_contents)
		return {'code':1,'msg':'suc'}

	def json_to_db_reportuuid(self,uuid_db_param):
		try:
			sql='insert into reportuuid(uuid,project_name,project_version,exec_time)VALUES (%s,%s,%s,%s)'
			mysqlhelper.insert(sql=sql, params=uuid_db_param)
			return success_desc("reportuuid数据插入成功")
		except:
			return false_desc("reportuuid数据插入失败")
	#获取最新的UUID 字符串
	def search_new_uuid(self):
		sql = 'select uuid from reportuuid order by report_uuid_id desc limit 1'
		uuid_param_tuple = mysqlhelper.get_one(sql=sql)
		uuid_param_str=uuid_param_tuple[0]
		return uuid_param_str

	def get_uuid_db_infa(self,id):
		pass

	#获取infatest表的数据条数
	def get_infatest_count(self,pro_uuid):
		'''
		((2,), (3,))
		((2,),)
		()
		:return:
		'''
		try:
			sql='select id from infatest where uuid=%s'
			params=(pro_uuid,)
			ids=mysqlhelper.get_all(sql,params)
			id_list=[]
			for id in ids:
				if id==():
					return ReturnDesc([]).success_desc()
				else:
					id_list.append(id[0])

			return ReturnDesc(id_list).success_desc()
		except:
			return ReturnDesc("获取用例id失败",902).false_desc()

	#获取online需要格式报告
	def get_online_report(self,pro_uuid):
		# table_truncate_result=mysqlhelper.table_truncate('reporttoonline')
		# if table_truncate_result['code']==1:
		fail_detail_list=[]
		sql='select id,exec_result,exec_time,uuid from infatest where uuid=%s'
		sql_insert='insert into reporttoonline(id,result,fail_detail,exec_time,uuid)values(%s,%s,%s,%s,%s)'
		get_online_report_params=(pro_uuid,)
		get_online_report_tuples=mysqlhelper.get_all(sql=sql,params=get_online_report_params)
		for get_online_report_tuple in get_online_report_tuples:
			get_online_report_list=list(get_online_report_tuple)
			logger.debug(get_online_report_list)
			if get_online_report_list[1]:
				if 'fail' in get_online_report_list[1]:
					logger.debug(get_online_report_list[1])
					get_online_report_list_child=json.loads(get_online_report_list[1])
					logger.debug(get_online_report_list_child)
					logger.debug(type(get_online_report_list_child))
					for fail_detail_value in get_online_report_list_child:
						logger.debug(fail_detail_value)
						logger.debug(type(fail_detail_value))
						if 'fail' == fail_detail_value['msg']:   #  in fail_detail_value:
							fail_detail_list.append(fail_detail_value)
							logger.debug(fail_detail_value)
					get_online_report_list[1]='fail'
				else:
					get_online_report_list[1] = 'pass'
				get_online_report_list.insert(-2, json.dumps(fail_detail_list,ensure_ascii=False))
				get_online_report_tuple=tuple(get_online_report_list)
				logger.debug(get_online_report_tuple)
				mysqlhelper.insert(sql=sql_insert,params=get_online_report_tuple)
				fail_detail_list = []
			else:
				return false_desc("实际测试结果为空")
		return success()
		# else:
		# 	return false_desc("清空表数据失败")

	# 获取online需要格式报告
	def get_online_report_v1(self, get_online_report):
		# table_truncate_result=mysqlhelper.table_truncate('reporttoonline')
		# if table_truncate_result['code']==1:
		fail_detail_list = []
		# sql = 'select id,exec_result,exec_time,uuid from infatest where uuid=%s'
		# sql_insert = 'insert into reporttoonline(id,result,fail_detail,exec_time,uuid)values(%s,%s,%s,%s,%s)'
		# get_online_report_params = (pro_uuid,)
		# get_online_report_tuples = mysqlhelper.get_all(sql=sql, params=get_online_report_params)
		# for get_online_report_tuple in get_online_report_tuples:
		# 	get_online_report_list = list(get_online_report_tuple)
		# 	logger.debug(get_online_report_list)
		get_online_report=json.dumps(get_online_report)
		if get_online_report:
			if 'fail' in get_online_report:
				logger.debug(get_online_report)
				get_online_report_list_child = json.loads(get_online_report)
				logger.debug(get_online_report_list_child)
				logger.debug(type(get_online_report_list_child))
				for fail_detail_value in get_online_report_list_child[0]:
					logger.debug(fail_detail_value)
					logger.debug(type(fail_detail_value))
					if 'fail' == fail_detail_value['msg']:  # in fail_detail_value:
						fail_detail_list.append(fail_detail_value)
						logger.debug(fail_detail_value)
				get_online_report_result = 'fail'
			else:
				get_online_report_result = 'pass'
			# get_online_report_list.insert(-2, json.dumps(fail_detail_list, ensure_ascii=False))
			# get_online_report_tuple = tuple(get_online_report_list)
			# logger.debug(get_online_report_tuple)
			# mysqlhelper.insert(sql=sql_insert, params=get_online_report_tuple)
			result_online_report = [fail_detail_list,get_online_report_result]
			return ReturnDesc(result_online_report).success_desc()
		else:
			return false_desc("实际测试结果为空")
		# return success()

	# else:
	# 	return false_desc("清空表数据失败")



	#获取online报告中的数据
	def get_online_data(self,pro_uuid):
		sql='select id,result,fail_detail,exec_time from reporttoonline where uuid=%s'
		params=(pro_uuid,)
		get_online_data_tuples=mysqlhelper.get_all(sql=sql,params=params)
		return get_online_data_tuples

	# 获取详细报告中的数据
	def get_detailreporthistory_data(self,pro_uuid,id=None):
		if id is None:
			sql = 'select id,detail_exec_result,exec_time from detailreporthistory where uuid=%s and id = %s'
			params = (pro_uuid, id)
			all_test_report=mysqlhelper.get_all(sql=sql, params=params)
			return all_test_report
		else:
			sql='select id,detail_exec_result,exec_time from detailreporthistory where uuid=%s and id = %s'
			params=(pro_uuid,id)
			id_test_report=mysqlhelper.get_all(sql=sql,params=params)
			return id_test_report

	#替换字符串中括号{}内的值
	def replace_str(self,dict_data, str_data):
		inexistence_list=[]
		if not isinstance(str_data,str):
			str_data=json.dumps(str_data,ensure_ascii=False).replace('\n', '').replace('\t', '').replace(' ', '')
		for key_dict, value_dict in dict_data.items():
			if "_int" in key_dict:
				key_dict = key_dict[:-4]
				if str_data[1]=='"':
					key_dict = '"{' + key_dict + '}"'
				elif str_data[1]=="'":
					key_dict = "'{" + key_dict + "}'"
				else:
					return ReturnDesc("替换json串中的参数错误"+key_dict,702).false_desc()
			else:
				key_dict = '{' + key_dict + '}'
			key_dict = key_dict.replace('\n', '').replace('\t', '').replace(' ', '')
			logger.debug(key_dict)
			if key_dict in str_data:
				logger.debug("key_dict in str_data")
				temporary = str_data.replace(key_dict, value_dict)
				logger.debug(temporary)
				str_data = temporary
			else:
				inexistence_list.append(key_dict)
		if inexistence_list==[]:
			return ReturnDesc(str_data).success_desc()
		else:
			return ReturnDesc("参数名不匹配："+str(inexistence_list),808).false_desc()

	#将两个列表匹配成字典
	def list_to_dict(self,list_keys,list_values):
		index_key=0
		dict_data={}
		for list_key in list_keys:
			dict_data[list_key]=list_values[index_key]
			index_key+=1
		return dict_data
	#jsonpath在字符串中获取键的值
	def path(self,string_data,grammar):
		import jsonpath
		grammar = grammar.replace('\n', '').replace('\t', '').replace(' ', '')
		jsonpath_result= jsonpath.jsonpath(string_data, grammar)
		if jsonpath_result:
			return jsonpath_result[0]
		else:
			false_desc("未找到匹配项")

	#字符串去除\n \t 空格
	def clear_string(self,string_data):
		if isinstance(string_data,str):
			string_data=string_data.replace('\n', '').replace('\t', '').replace(' ', '')
			return string_data
		else:
			return string_data

	#字符串转换python其他类型
	def data_type_conversion(self,dataed, data):

		logger.debug(type(dataed))
		logger.debug(type(data))
		if isinstance(dataed, str):
			dataed=self.clear_string(dataed)
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
					return ReturnDesc(desc="预期参数结果错误"+dataed,code=701).false_desc()
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





#促销接口参数
{
	"merchant": 0,
	"label": 1,
	"storeId": "0620",
	"channelId": 0,
	"memberId": "99470100014083",
	"memberType": "98|1|201|202|106",
	"orderId": "1",
	"goodsList": [{
		"rowNo": 1,
		"quantity": 5555,
		"salePrice": 1200,
		"isWeigh": 0,
		"goodsCode": "740513",
		"sku": "740513",
		"goodsName": "两件减100A",
		"categoryCode": 458969,
		"brand": 1,
		"brandCode": 0
	}, {
		"rowNo": 2,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "015175",
		"sku": "015175",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 3,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "015175",
		"sku": "015175",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 4,
		"quantity": 455,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "015175",
		"sku": "015175",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 5,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "854251",
		"sku": "854251",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 6,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "338412",
		"sku": "338412",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 7,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "337679",
		"sku": "337679",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 8,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "269011",
		"sku": "269011",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 9,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "035553",
		"sku": "035553",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 10,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "015175",
		"sku": "015175",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 11,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "337716",
		"sku": "337716",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 12,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "740368",
		"sku": "740368",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 13,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "337654",
		"sku": "337654",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 14,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "771915",
		"sku": "771915",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}, {
		"rowNo": 15,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "771915",
		"sku": "771915",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}
	]
}
#阉割版
{
	"merchant": 0,
	"label": 1,
	"storeId": "0620",
	"channelId": 0,
	"memberId": "99470100014083",
	"memberType": "98|1|201|202|106",
	"orderId": "1",
	"goodsList": [{
		"rowNo": 1,
		"quantity": 5555,
		"salePrice": 1200,
		"isWeigh": 0,
		"goodsCode": "740513",
		"sku": "740513",
		"goodsName": "两件减100A",
		"categoryCode": 458969,
		"brand": 1,
		"brandCode": 0
	}, {
		"rowNo": 2,
		"quantity": 5,
		"salePrice": 15000,
		"isWeigh": 0,
		"goodsCode": "015175",
		"sku": "015175",
		"goodsName": "两件减100B",
		"brand": 1,
		"categoryCode": 36,
		"brandCode": 0

	}
	]
}
#促销接口返回参数
{
    "responseCode": "SUC",
    "responseMsg": "success",
    "requestId": "111",
    "timestamp": "1536630778508",
    "dataKey": 'null',
    "data": {
        "goodsResultList": [
            {
                "goodsId": "740513",
                "rowNum": 1,
                "ruleResults": [
                    {
                        "promotionNum": "620700141823",
                        "promotionName": "买一送一",
                        "quantity": 5554,
                        "promGoods": 'null',
                        "promotionType": 3,
                        "promotionAmount": 3332400,
                        "promotionShare": 'null',
                        "promotionDesc": "买一送一"
                    }
                ],
                "promotionTotalAmount": 'null',
                "totalDiscount": 3332400
            },
            {
                "goodsId": "854251",
                "rowNum": 5,
                "ruleResults": [
                    {
                        "promotionNum": "620700141633",
                        "promotionName": "8折",
                        "quantity": 5,
                        "promGoods": 'null',
                        "promotionType": 3,
                        "promotionAmount": 15000,
                        "promotionShare": 'null',
                        "promotionDesc": "8折"
                    }
                ],
                "promotionTotalAmount": 'null',
                "totalDiscount": 15000
            },
            {
                "goodsId": "771915",
                "rowNum": 15,
                "ruleResults": [
                    {
                        "promotionNum": "620700141804",
                        "promotionName": "买一送一",
                        "quantity": 5,
                        "promGoods": 'null',
                        "promotionType": 3,
                        "promotionAmount": 75000,
                        "promotionShare": 'null',
                        "promotionDesc": "买一送一"
                    },
                    {
                        "promotionNum": "620700141804",
                        "promotionName": "买一送一",
                        "quantity": 5,
                        "promGoods": 'null',
                        "promotionType": 3,
                        "promotionAmount": 75000,
                        "promotionShare": 'null',
                        "promotionDesc": "买一送一"
                    },
                    {
                        "promotionNum": "620700141804",
                        "promotionName": "买一送一",
                        "quantity": 5,
                        "promGoods": 'null',
                        "promotionType": 3,
                        "promotionAmount": 75000,
                        "promotionShare": 'null',
                        "promotionDesc": "买一送一"
                    },
                    {
                        "promotionNum": "620700141804",
                        "promotionName": "买一送一",
                        "quantity": 5,
                        "promGoods": 'null',
                        "promotionType": 3,
                        "promotionAmount": 75000,
                        "promotionShare": 'null',
                        "promotionDesc": "买一送一"
                    }
                ],
                "promotionTotalAmount": 'null',
                "totalDiscount": 300000
            }
        ],
        "tenders": [],
        "quotaManager": 'null'
    }
}
#阉割版
{
    "responseCode": "SUC",
    "responseMsg": "success",
    "requestId": "111",
    "timestamp": "1536638051586",
    "dataKey": 'null',
    "data": {
        "goodsResultList": [
            {
                "goodsId": "740513",
                "rowNum": 1,
                "ruleResults": [
                    {
                        "promotionNum": "620700141823",
                        "promotionName": "买一送一",
                        "quantity": 5554,
                        "promGoods":  'null',
                        "promotionType": 3,
                        "promotionAmount": 3332400,
                        "promotionShare":  'null',
                        "promotionDesc": "买一送一"
                    }
                ],
                "promotionTotalAmount":  'null',
                "totalDiscount": 3332400
            }
        ],
        "tenders": [],
        "quotaManager":  'null'
    }
}
#促销接口访问地址
url_promotion='http://192.168.2.55:8060/wise-promotion-query-service/multiQuery/0/0620'
json_test_params={
	"project_name":"picking",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"接口名称":"post_json接口测试",
		"method":"post_json",
		"URL":"http://127.0.0.1:5000/admin/api/infa/test3",
		"用例描述":"test",
		"用例参数":"test1:test_test01;test2:test_test02;",
		"预期结果":"test1:test_test01;test2:test_test02;",
		"json传参示例":'{"test1": "{test1}", "test2": "{test2}"}'},
		{"id": 1,
		 "接口名称": "post_json接口测试",
		 "method": "post_json",
		 "URL": "http://127.0.0.1:5000/admin/api/infa/test3",
		 "用例描述": "test",
		 "用例参数": "test1:test_test01;test2:test_test02;",
		 "预期结果": "test1:test_test01;test2:test_test02;",
		 "json传参示例": '{"test1": "{test1}", "test2": "{test2}"}'},
	]
}

#json接受平台数据格式——测试篇
#接口测试1
{
	"project_name":"picking",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"post_json接口测试",
		"method":"post_json",
		"URL":"http://127.0.0.1:5000/admin/api/infa/test3",
		"test_descript":"test",
		"test_params":"test1:test_test01;test2:test_test02;",
		"except_descript":"test1:test_test01;test2:test_test02;",
		"example_json_params":"{'test1': '{test1}', 'test2': '{test2}'}"}
	]
}
#接口测试2 post—json格式 返回格式为json
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"促销接口测试",
		"method":"post_json",
		"URL":"http://192.168.2.55:8060/wise-promotion-query-service/multiQuery/0/0620",
		"test_descript":"test",
		"test_params":"merchant:0; storeId:0620; channelId:0; memberId:0; quantity: 5555;salePrice: 1200;goodsCode: 740513;sku:740513;quantity0: 5;salePrice0: 15000;goodsCode0: 015175;sku0: 015175",
		"except_descript":"responseCode: SUC;responseMsg: success; goodsId: 740513;",
		"example_json_params":{
			"merchant": "{merchant}",
			"label": 1,
			"storeId": "{storeId}",
			"channelId": "{channelId}",
			"memberId": "{memberId}",
			"memberType": "98|1|201|202|106",
			"orderId": "1",
			"goodsList": [{
				"rowNo": 1,
				"quantity": "{quantity}",
				"salePrice": "{salePrice}",
				"isWeigh": 0,
				"goodsCode": "{goodsCode}",
				"sku": "{sku}",
				"goodsName": "两件减100A",
				"categoryCode": 458969,
				"brand": 1,
				"brandCode": 0
			}, {
				"rowNo": 2,
				"quantity": "{quantity0}",
				"salePrice": "{salePrice0}",
				"isWeigh": 0,
				"goodsCode": "{goodsCode0}",
				"sku": "{sku0}",
				"goodsName": "两件减100B",
				"brand": 1,
				"categoryCode": 36,
				"brandCode": 0

			}
			]
		}
		}
	]
}
#接口三 post—json格式 返回格式为json url为拼接格式
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"促销接口测试",
		"method":"post_json",
		"URL":"http://192.168.2.55:8060/wise-promotion-query-service/multiQuery/{memberIdURL}/{storeIdURL}",
		"test_descript":"test",
		"test_params":"storeIdURL:0620;memberIdURL:0;merchant:0; storeId:0620; channelId:0; memberId:0; quantity: 5555;salePrice: 1200;goodsCode: 740513;sku:740513;quantity0: 5;salePrice0: 15000;goodsCode0: 015175;sku0: 015175",
		"except_descript":"responseCode: SUC;responseMsg: success; goodsId: 740513;",
		"example_json_params":{
			"merchant": "{merchant}",
			"label": 1,
			"storeId": "{storeId}",
			"channelId": "{channelId}",
			"memberId": "{memberId}",
			"memberType": "98|1|201|202|106",
			"orderId": "1",
			"goodsList": [{
				"rowNo": 1,
				"quantity": "{quantity}",
				"salePrice": "{salePrice}",
				"isWeigh": 0,
				"goodsCode": "{goodsCode}",
				"sku": "{sku}",
				"goodsName": "两件减100A",
				"categoryCode": 458969,
				"brand": 1,
				"brandCode": 0
			}, {
				"rowNo": 2,
				"quantity": "{quantity0}",
				"salePrice": "{salePrice0}",
				"isWeigh": 0,
				"goodsCode": "{goodsCode0}",
				"sku": "{sku0}",
				"goodsName": "两件减100B",
				"brand": 1,
				"categoryCode": 36,
				"brandCode": 0

			}
			]
		}
		}
	]
}
#接口四 get请求，无参数
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/2/getMaxBindingGoods?pagenum=1&pagesize=2",
		"test_descript":"test",
		"test_params":"",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		}
	]
}
#接口五 get请求，有参数
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/2/getMaxBindingGoods",
		"test_descript":"test",
		"test_params":"pagesize:2;pagenum:1;",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		}
	]
}
#接口六 get请求，url带参数
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/{api}/getMaxBindingGoods?pagenum={pagenum}&pagesize={pagesize}",
		"test_descript":"test",
		"test_params":"api:2;pagesize:2;pagenum:1;",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		}
	]
}
#接口七 get请求，url？后参数分开写入用例描述和url中
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/2/getMaxBindingGoods?pagenum={pagenum}",
		"test_descript":"test",
		"test_params":"pagesize:2;pagenum:1;",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		}
	]
}
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/2/getMaxBindingGoods",
		"test_descript":"test",
		"test_params":"pagesize:2;pagenum:1;",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		},{"id":2,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/{api}/getMaxBindingGoods?pagenum={pagenum}&pagesize={pagesize}",
		"test_descript":"test",
		"test_params":"api:2;pagesize:2;pagenum:1;",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		},{"id":3,
		"infa_name":"get请求，无参数",
		"method":"get",
		"URL":"http://192.168.2.241:8081/shopweb01/ogi/stores/2/getMaxBindingGoods?pagenum={pagenum}",
		"test_descript":"test",
		"test_params":"pagesize:2;pagenum:1;",
		"except_descript":"code: 1001;msg: success; itemPerPage: 2;totalPage:19;totalAmount:37;",
		"example_json_params":""
		}
	]
}
#接口八 post请求，url无参数，有参数，参数化，多个case
{
	"project_name":"Promotion_wise",
	"project_version":"rc1",
	"test_param":[
		{"id":1,
		"infa_name":"get请求，无参数",
		"method":"post",
		"URL":"http://www.httpbin.org/post",
		"test_descript":"test",
		"test_params":"pagesize:2;pagenum:1;",
		"except_descript":"pagesize:2;pagenum:1;",
		"example_json_params":""
		},{"id":2,
		"infa_name":"get请求，无参数",
		"method":"post",
		"URL":"http://www.httpbin.org/post?name={name}&age={age}",
		"test_descript":"test",
		"test_params":"name:xiaoming;age:81;pagesize:2;pagenum:1;",
		"except_descript":"name:xiaoming;age:81;pagesize:2;pagenum:1;",
		"example_json_params":""
		},{"id":3,
		"infa_name":"get请求，无参数",
		"method":"post",
		"URL":"http://www.httpbin.org/post?name={name}",
		"test_descript":"test",
		"test_params":"name:xiaoming;age:81;pagesize:2;pagenum:1;",
		"except_descript":"name:xiaoming;age:81;pagesize:2;pagenum:1;",
		"example_json_params":""
		}
	]
}

'''
1.接受参数
2.将参数存放到目录表、测试表，测试历史表
3.生成测试结果，将测试结果存放到测试表、测试历史表
4.将测试表结果数据整个存放到详细报告表
5.将测试表中的结果存放到返回报告表中
6.将返回报告表中的数据返回给平台
'''
def infaPostTest(params):
	sql="insert into users(name,email,pswd)values(%s,%s,%s)"

	mysqlhelper.insert(sql,params)


dict_test={"params":(("wang","wang@163.com","123456"),
                     ("zhang","zhang@189.com","201512"),
                     ("chen","chen@126.com","987654"),
                     ("zhou","zhou@163.com","456789"))
}




if __name__=='__main__':
	# params=dict_test["params"]
	# # params=(('wang','wang@163.com','123456'),('zhang','zhang@189.com','201512'),('chen','chen@126.com','987654'),('zhou','zhou@163.com','456789'))
	# # logger.debug(params)
	# infaPostTest(params)
	# a=(('wang', 'wang@163.com', '123456'), ('zhang', 'zhang@189.com', '201512'), ('chen', 'chen@126.com', '987654'),
	#  ('zhou', 'zhou@163.com', '456789'))
	# b=str(a)
	# print(b)
	# print(type(b))
	# c=eval(b)
	# infaPostTest(c)
	# data=(('"36e9dd4f-eb4a-45a0-9def-29ae686a002a"', 'Promotion_wise', 'rc1', 1, 'get请求，无参数',
	#        'post', 'http://www.httpbin.org/post', 'test', 'pagesize:2;pagenum:1;', 'pagesize:2;pagenum:1;', '""',
	#        '{"ErroCode": null, "Msg": "Suc", "code": 1, "desc": {"pagenum": "1", "pagesize": "2"}}', 'pass', '[]',
	#        datetime(2018, 10, 11, 17, 46, 0, 871091)),
	#       ('"36e9dd4f-eb4a-45a0-9def-29ae686a002a"', 'Promotion_wise', 'rc1', 1, 'get请求，无参数', 'post',
	#        'http://www.httpbin.org/post', 'test', 'pagesize:2;pagenum:1;', 'pagesize:2;pagenum:1;', '""',
	#        '{"ErroCode": null, "Msg": "Suc", "code": 1, "desc": {"pagenum": "1", "pagesize": "2"}}', 'pass',
	#        '[]', datetime(2018, 10, 11, 17, 46, 0, 871091)),
	#       ('"36e9dd4f-eb4a-45a0-9def-29ae686a002a"', 'Promotion_wise', 'rc1', 2, 'get请求，无参数',
	#        'post', 'http://www.httpbin.org/post?name={name}&age={age}', 'test', 'name:xiaoming;age:81;pagesize:2;pagenum:1;',
	#        'name:xiaoming;age:81;pagesize:2;pagenum:1;', '""', '{"ErroCode": null, "Msg": "Suc", "code": 1, "desc": {"age": '
	#                                                            '"81", "name": "xiaoming", "pagenum": "1", "pagesize": "2"}}', 'pass', '[]',
	#        datetime(2018, 10, 11, 17, 46, 1, 501400)),
	#       ('"36e9dd4f-eb4a-45a0-9def-29ae686a002a"',
	#        'Promotion_wise', 'rc1', 1, 'get请求，无参数', 'post', 'http://www.httpbin.org/post', 'test',
	#        'pagesize:2;pagenum:1;', 'pagesize:2;pagenum:1;', '""', '{"ErroCode": null, "Msg": "Suc", "code": 1, '
	#                                                                '"desc": {"pagenum": "1", "pagesize": "2"}}', 'pass', '[]',
	#        datetime(2018, 10, 11, 17, 46, 0, 871091)),
	#       ('"36e9dd4f-eb4a-45a0-9def-29ae686a002a"', 'Promotion_wise', 'rc1', 2, 'get请求，无参数', 'post',
	#        'http://www.httpbin.org/post?name={name}&age={age}', 'test', 'name:xiaoming;age:81;pagesize:2;pagenum:1;',
	#        'name:xiaoming;age:81;pagesize:2;pagenum:1;', '""', '{"ErroCode": null, "Msg": "Suc", "code": 1, "desc":'
	#                                                            ' {"age": "81", "name": "xiaoming", "pagenum": "1", "pagesize": "2"}}',
	#        'pass', '[]', datetime(2018, 10, 11, 17, 46, 1, 501400)),
	#       ( '"36e9dd4f-eb4a-45a0-9def-29ae686a002a"', 'Promotion_wise',
	#         'rc1', 3, 'get请求，无参数', 'post', 'http://www.httpbin.org/post?name={name}', 'test', 'name:xiaoming;age:81;pagesize:2;pagenum:1;',
	#         'name:xiaoming;age:81;pagesize:2;pagenum:1;', '""', '{"ErroCode": null, "Msg": "Suc", "code": 1, "desc":'
	#                                                             ' {"age": "81", "name": "xiaoming", "pagenum": "1", "pagesize": "2"}}', 'pass', '[]',
	#         datetime(2018, 10, 11, 17, 46, 2, 72631)))
	# pool = multiprocessing.Pool(multiprocessing.cpu_count())
	# a=Tools()#.json_to_db_test_report(json_contents=data)
	# for i in range(50):
	# 	pool.map(a.json_to_db_test_report, data)
	# # print(a)
	# a={
	# "code": 1001,
	# "msg": "success",
	# "data": [
     #    {
     #        "id": 2,
     #        "storeCode": "1000",
     #        "name": "shopweb01_1000",
     #        "customerStoreCode": "1000",
     #        "storeIPAddress": None,
     #        "status": 1,
     #        "address": None
     #    },
     #    {
     #        "id": 3,
     #        "storeCode": "1001",
     #        "name": "shopweb01_1001",
     #        "customerStoreCode": "1001",
     #        "storeIPAddress": None,
     #        "status": 1,
     #        "address": None
     #    },
     #    {
     #        "id": 4,
     #        "storeCode": "666",
     #        "name": "莉娟test门店",
     #        "customerStoreCode": "666",
     #        "storeIPAddress": None,
     #        "status": 1,
     #        "address": "阿士大夫士大夫士大夫的说法都是撒范德萨的"
     #    }
	# ]
	# }
	# a=json.dumps(a)
	# a = json.loads(a)
	# # b=Tools().path(string_data=a, grammar="$..id")
	# # print(b)
	# # print(str(a).count("id"))
	#
	# except_name="id"
	# b=SoursDeal().end_mark_re(except_name, str_data=str(a))
	# print(b)

	test=['"a15d81d6-8ba8-495b-8a37-96d7190770e4"', 'Promotion_wise', 'rc1', 1, '促销接口测试', 'get', 'http://192.168.2.241:8081/shopweb01/ogi/stores',
	      'test', '', 'code: 1001;msg:success;id:[2,3,4];storeCode:[1000,1001,666];', '""',
	      '{"ErroCode": null, "Msg": "Suc", "code": 1, "desc": {"code": "1001", "id": ["2", "3", "4"],'
	      ' "msg": "success", "storeCode": ["1000", "1001", "666"]}}', 'pass', '[]', datetime.datetime(2018, 10, 19, 13, 40, 31, 306968)]

	test=json.dumps(test)
	a=SoursDeal().end_mark_re_v1(except_name="storeCode", str_data=test)
	print(a)