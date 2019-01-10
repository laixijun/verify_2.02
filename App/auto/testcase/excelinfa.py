import os
import shutil
from time import time

import requests
import xlrd
import xlwt
from flask import json
from xlutils.copy import copy

class ExcelRW(object):
    # def __init__(self,dir=test_file_xlsx,sheet_name=sheet_name,write_sheet=write_sheet):
    def __init__(self, dir="", sheet_name="", write_sheet=""):
        self.url=dir
        self.sheet_name=sheet_name
        self.write_sheet=write_sheet
        self.workbook = xlrd.open_workbook(self.url)  #获取读文件
        self.sheet_names = self.workbook.sheet_names()  #获取所有的读sheet
        self.sheet = self.workbook.sheet_by_name(self.sheet_name) #获取读sheet
        self.wbk = xlwt.Workbook(encoding='utf8') #获取写文件
        self.sheet_write=self.wbk.add_sheet(self.write_sheet,cell_overwrite_ok=False) #获取写sheet
        self.co = copy(self.workbook)

    #读取指定位置的值
    def read_cell(self,row_index,col_index):
        result=self.sheet.cell_value(row_index,col_index)
        return result

    # 读取指定行位置的值
    def rows(self):
        rows = self.sheet.nrows
        return rows

    # 读取指定列位置的值
    def cols(self):
        cols = self.sheet.ncols
        return cols

    # 读取指定行rows的值
    def read_row(self,row_index):
        row_list = self.sheet.row_values(row_index)
        return row_list

    # 读取指定列cols的值
    def read_col(self,col_index):
        col_list = self.sheet.col_values(col_index)
        return col_list

    #按行写每行
    # results需要写入的内容
    # row_num每行多少个
    #write_url excel 保存的路径
    def write_cell(self,results,row_num,write_url):
        # 控制行的位置
        column = 0
        row = 0
        # 生成第一行
        for result in results:
            # 参数对应：行，列，值，字体样式(可以没有)
            self.sheet_write.write(column, row, result)
            # 这里主要为了控制输入每行十个内容。为了查看
            row += 1
            if row % row_num == 0:
                column += 1
                row = 0
        self.wbk.save(write_url)

    #修改excel表格
    def alter(self,x,y,content):
        num=self.sheet_names.index(self.write_sheet)
        write_el=self.co.get_sheet(num)
        write_el.write(x,y,content)
    #保存Excel表格
    def save(self):
        self.co.save(self.url)
class TestExcelINFA(object):
	def __init__(self):
		pass
	#复制报告模板命名为testdata
	def copyfile_path_v1(self,oldpathfile, newpathfile):
		# newpathfile=path_test_report(pro='test')
		shutil.copy(oldpathfile, newpathfile)
		return {'code': 1, 'msg': 'success'}

	# 修改指定文件的文件名
	def rename(self, filename, newname):
		# path = path  # 文件路径(\注意使用转义字符)
		# filename = os.path.join(path, filename)  # 旧文件名
		# newname = os.path.join(path, newname)  # 新文件名
		os.rename(filename, newname)

	#读取数据，生成接口服务器接受的格式
	def readData(self):
		excelrd=ExcelRW(dir="infadata.xls", sheet_name="infadata",write_sheet="infadata")
		readdata_dict={}
		test_param=[]
		readdata_dict_dict={}
		readdata_dict_dict_dict = {}
		readdata_dict_dict_dict_dict = {}
		readdata_dict["project_name"]=excelrd.read_cell(1,0)
		readdata_dict["project_version"] = excelrd.read_cell(1, 1)
		rows_index=excelrd.rows()
		for row_index in range(1,rows_index):
			row_list=excelrd.read_row(row_index)
			readdata_dict_dict["id"] = int(row_list[2])
			readdata_dict_dict["infa_name"] = row_list[3]
			readdata_dict_dict["method"] = row_list[4]
			row_list_data=row_list[5].replace('\n', '').replace('\t', '').replace(' ', '')
			readdata_dict_dict["URL"] = row_list_data
			readdata_dict_dict["test_descript"] = row_list[6]
			readdata_dict_dict["test_params"] = row_list[7]
			readdata_dict_dict["except_descript"] = row_list[8]
			readdata_dict_dict["example_json_params"] = row_list[9]
			id_dict=str(readdata_dict_dict["id"])
			readdata_dict_dict_dict[id_dict]=[readdata_dict_dict["URL"],readdata_dict_dict["test_descript"]]
			test_param.append(readdata_dict_dict)
			readdata_dict_dict={}

		readdata_dict["test_param"] = test_param
		readdata_dict_dict_dict_dict["post_json"]=readdata_dict
		readdata_dict_dict_dict_dict["id"]=readdata_dict_dict_dict
		return readdata_dict_dict_dict_dict

	#请求接口，接收测试结果
	def infaData(self,readdata):
		url="http://192.168.2.10:8088/user/api/push_v1"
		#url = "http://127.0.0.1:5000/user/api/push_v1"
		data=json.dumps(readdata,ensure_ascii=False)
		print(data)
		headers = {
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
		}
		resp = requests.post(url=url, data=data.encode(), headers=headers)
		resp_loads=json.loads(resp.text)
		return resp_loads

	#将测试结果存放到Excel
	def saveData(self,infadata,rdid):
		x=1
		y=0
		excelrd = ExcelRW(dir="testdata.xls", sheet_name="testdata", write_sheet="testdata")
		if infadata["code"]==0:
			excelrd.alter(1, 0, infadata)
			return infadata
		elif infadata["code"]==1:
			for results in infadata["result"]:
				excelrd.alter(x,y,infadata["project_name"])
				y+=1
				excelrd.alter(x, y, infadata["project_version"])
				y+=1
				excelrd.alter(x, y, infadata["uuid"])
				y += 1
				excelrd.alter(x, y, results["id"])
				y += 1
				param_id=str(results["id"])
				excelrd.alter(x, y, rdid[param_id][0])
				y += 1
				excelrd.alter(x, y, rdid[param_id][1])
				y += 1
				excelrd.alter(x, y, json.dumps(results["error_result"]))
				y += 1
				excelrd.alter(x, y, results["exec_result"])
				y += 1
				excelrd.alter(x, y, results["exec_time"])
				y += 1
				x+=1
				y=0
			excelrd.save()
			return {"code":1,"msg":"suc"}


	def exeTest(self):
		self.copyfile_path_v1(oldpathfile="testdata_m.xls", newpathfile="testdata.xls")
		readdata=self.readData()
		if readdata:
			print(readdata)
			readdata_param=readdata["post_json"]
			readdata_id = readdata["id"]
			infadata=self.infaData(readdata=readdata_param)
			if infadata:
				print(infadata)
				self.saveData(infadata,rdid=readdata_id)
				newpathfile="testdata"+str(int(time()))+".xls"
				self.rename(filename="testdata.xls", newname=newpathfile)
				return newpathfile

if __name__=="__main__":
	a=TestExcelINFA().exeTest()
	print(a)
