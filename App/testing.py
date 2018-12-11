import paramiko

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

if __name__=='__main__':
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
	# # sftp(ip, port, username, passwd, method, local, motive)
	# print(a)
	# # input()
	a=[]
	print(len(a))