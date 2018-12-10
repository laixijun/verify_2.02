import threading

import paramiko


def threadingTimer(time,func):
	timer = threading.Timer(time, func)
	timer.start()


class RemoteSource:
	def __init__(self):
		pass
	#远程读取服务器文件
	def ssh(ip, username, passwd, cmd):
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
			return result.decode()
			ssh.close()
		except:
			print('%s\tError\n' % (ip))
	#远程服务器下载文件到本地
	def sftp(ip, port, username, passwd, method, local, motive):
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