import threading
import paramiko
import winrm
import json

from libs.error_code import ReturnDesc, ERRRecord
from log.logging_file_console import logger


def threadingTimer(time,func):
	timer = threading.Timer(time, func)
	timer.start()




"""
#cmd = ['find /home/admin/logs/ -mtime +3 -name \'*.log.*\' -exec rm -rf {} \;']#你要执行的命令列表
	cmd = ['cat /tmp/zhy/a.log']#你要执行的命令列表
	username = "root"  #用户名
	passwd = "123456"    #密码
	threads = []   #多线程
	ip = "192.168.31.118"
	print("Begin......")
	port=22
	method="get"
	local="C:/Users/zhy/Desktop/a.log"
	motive="/tmp/zhy/a.log"
	# a=threading.Thread(target=ssh,args=(ip,username,passwd,cmd))
	# a.start()
	# a=ssh(ip,username,passwd,cmd)
	sftp(ip, port, username, passwd, method, local, motive)
	# print(a)
	# input()
"""
class RemoteSource:
	def __init__(self):
		pass
	#远程读取服务器文件
	def ssh1(self,ip, username, passwd, cmd):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip, 22, username, passwd, timeout=5)
			for m in cmd:
				stdin, stdout, stderr = ssh.exec_command(m)
				res = stdout.read()  # 屏幕输出
				err = stderr.read()
				result = res if res else err
			print('%s\tOK\n' % (ip))
			ssh.close()
			if result:
				return ReturnDesc(desc=result.decode()).success_desc()
			else:
				return ReturnDesc(desc=ERRRecord.REMOTEFILECONTENT, code=ERRRecord.REMOTEFILECONTENTNO).false_desc()
		except:
			print('%s\tError\n' % (ip))
			return ReturnDesc(desc=ERRRecord.REMOTEFILE,code=ERRRecord.REMOTEFILENO).false_desc()

	def ssh(self,ip, username, passwd, cmd):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		print("ok")
		ssh.connect(ip, 22, username, passwd, timeout=30,allow_agent=False,look_for_keys=False)
		for m in cmd:
			stdin, stdout, stderr = ssh.exec_command(m)
			res = stdout.read()  # 屏幕输出
			err = stderr.read()
			result = res if res else err
			print(res,err)
		print('%s\tOK\n' % (ip))
		ssh.close()
		if result:
			return ReturnDesc(desc=result.decode()).success_desc()
		else:
			return ReturnDesc(desc=ERRRecord.REMOTEFILECONTENT, code=ERRRecord.REMOTEFILECONTENTNO).false_desc()

	#远程服务器下载文件到本地
	def sftp(self,ip, port, username, passwd, method, local, motive):
		try:
			transport = paramiko.Transport((ip, port))
			transport.connect(username=username, password=passwd)

			sftp = paramiko.SFTPClient.from_transport(transport)
			if method == "push":
				sftp.push(local, motive)
			elif method == "get":
				sftp.get(motive, local)
			print('%s\tOK\n' % (ip))
			transport.close()
		except:
			print('%s\tError\n' % (ip))

"""
paramiko, pywinrm实现windows/linux脚本调用
"""


class ServerByPara(object):
	def __init__(self, ip, username, passwd, cmd, system_choice):
		self.cmd = cmd
		self.client = paramiko.SSHClient()
		self.host = ip
		self.user = username
		self.pwd = passwd
		self.system_choice = system_choice

	def exec_linux_cmd(self):
		data_init = ''
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.client.connect(hostname=self.host,port=22, username=self.user, password=self.pwd)
		stdin, stdout, stderr = self.client.exec_command(self.cmd, get_pty=True)
		if stderr.readlines():
			exec_tag = 0
			for data in stdout.readlines():
				data_init += data
		else:
			exec_tag = 1
			for data in stdout.read().decode():
				data_init += data
		# data_init = json.dumps(data_init, ensure_ascii=False)
		return {
			"exec_tag": exec_tag,
			"data": data_init,
		}

	def exec_win_cmd(self):
		data_init = ""
		s = winrm.Session(self.host, auth=(self.user, self.pwd))
		ret = s.run_cmd(self.cmd)
		if ret.std_err.decode():
			exec_tag = 0
			# for data in ret.std_err.decode().split("\r\n"):
			for data in ret.std_err.decode():
				data_init += data
		else:
			exec_tag = 1
			# for data in ret.std_out.decode().split("\r\n"):
			for data in ret.std_out.decode():
				data_init += data
		# data_init=json.dumps(data_init,ensure_ascii=False)
		return {
			"exec_tag": exec_tag,
			"data": data_init,
		}


	def run(self):
		try:
			if self.system_choice == "Linux" or self.system_choice == "linux":
				logger.debug("linux...")
				result = self.exec_linux_cmd()
				logger.debug(result)
			else:
				result = self.exec_win_cmd()
				logger.debug(result)
		except:
			logger.debug('%s\tError\n' % (self.host))
			return ReturnDesc(desc=ERRRecord.REMOTEFILE, code=ERRRecord.REMOTEFILENO).false_desc()
		logger.debug('%s\tOK\n' % (self.host))
		if result["exec_tag"] == 1:
			if result["data"]:
				return ReturnDesc(desc=result["data"]).success_desc()
			else:
				return ReturnDesc(desc=ERRRecord.REMOTEFILECONTENT, code=ERRRecord.REMOTEFILECONTENTNO).false_desc()
		else:
			logger.debug('%s\tError\n' % (self.host))
			return ReturnDesc(desc=ERRRecord.REMOTEFILE, code=ERRRecord.REMOTEFILENO).false_desc()

# if __name__ == '__main__':
# server_obj = ServerByPara(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# server_obj = ServerByPara(r"C:\Users\a\Desktop\test.bat", "192.168.12.149", "a",
#                           "password", "Windows")
# server_obj = ServerByPara(r"/root/Desktop/test.sh >> log.txt", "192.168.109.132", "root",
#                           "password", "Linux")
# server_obj.run()


if __name__ == "__main__":
	# ip="192.168.7.50"
	# username="zhy"
	# passwd="123456"
	# cmd=["ls"]

	host="192.168.2.17"
	user="hanshow"
	passwd="hanshow"
	# cmd=["type C:/mysql_log.log"]
	system_choice="windows"
	cmd = "type C:\\mysql_log.log"

	# ip = "127.0.0.1"
	# username="zhy"
	# passwd="xyz.1117"
	# # cmd=["type C:/mysql_log.log"]
	# cmd = ['dir']

	sr=ServerByPara(host, user, passwd,cmd,  system_choice).run()
	# a=RemoteSource().ssh(ip, username, passwd, cmd)
	print(sr)