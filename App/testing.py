import json
import re

import paramiko


# a="2018-10-11T12:36:29.342279Z	   70 Query	SHOW COLUMNS FROM `flask_db`." \
#   "`new_report_test` (2018-10-11T12:47:47.382966Z)	    9 Quit	"

# regu='C:\\Program Files\\MySQL\\(.*?)\\bin'

# regular="SHOW(.*?)FROM"
# reg= re.compile(regu, re.S)
# reg_list=reg.findall(dict_data["desc"])
# print(reg_list)

import chardet
a='abc123'
b='中国'
a=a.encode('gbk')
b=b.encode('gbk').decode("gbk").encode("utf-8").decode()
for i in [a,b]:
	# print(i, chardet.detect(i))
	print(i)