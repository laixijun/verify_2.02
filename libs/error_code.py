def success():
	return {'code': 1, 'Msg': 'SUC'}

def false():
	return {'code': 0, 'Msg': 'FAIL'}

def success_desc(desc):
	return {'code': 1, 'Msg': 'Suc','desc':desc}

def false_desc(desc):
	return {'code': 0, 'Msg': 'Fail','desc':desc}

class ReturnDesc:
	def __init__(self,desc=None,code=None):
		self.desc=desc

		self.code=code

	def false_desc(self):
		return {'code': 0, 'Msg': 'Fail','desc':self.desc,'ErroCode':self.code}

	def success_desc(self):
		return {'code': 1, 'Msg': 'Suc', 'desc': self.desc,'ErroCode':self.code}


class ERRRecord:
	'''
	数据读写错误9开始
	传入参数有误8开始
	程序有误7开始

	'''
	#DB 和 FILE 查询生成测试结果，输入pro_uuid 错误
	DBSEARCHUUID="UUID 不存在"
	DBSEARCHUUIDNO = 8010

	# file日志文件读取失败
	REMOTEFILE="远程读取日志文件失败"
	REMOTEFILENO=703

	# file日志文件读取为空
	REMOTEFILECONTENT = "远程读取日志文件为空"
	REMOTEFILECONTENTNO = 8012

	# file日志文件正则匹配为空
	REMOTEFILERECONTENT = "日志文件正则匹配为空"
	REMOTEFILERECONTENTNO = 8013

	# file日志文件正则匹配值对比非字符串
	REMOTEFILERECOMPCONTENT = "日志匹配值对比非字符串"
	REMOTEFILERECOMPCONTENTNO = 8014

	# mysql测试数据读取失败
	REMOTEMYSQL="mysql测试数据读取失败"
	REMOTEMYSQLNO =704

	# mysql测试数据读取为空
	REMOTEMYSQLCONTENT = "mysql测试数据读取失败"
	REMOTEMYSQLCONTENTNO = 8011

	def record(self):
		{
			"获取db中url失败": 901,
			"传入用例参数格式有误":801,
			'传入参数格式不正确或未传入参数':802,
			'参数无用例列表或用例列表格式不正确':803,
			'列表中的用例，必填项未正确填写':804,
			'列表中的用例id重复 ':805,
			"url给出的参数名与用例中的参数名不匹配":806,
			"url错误":807,
			"参数名不匹配：":808,
			"获取用例id失败":902,
			"请求方式传参错误 ":809,
			"预期参数结果错误":701,
			"替换json串中的参数错误":702,
			"请求成功":1
		}
