

class TerminalDeal:

	def __init__(self):
		pass

	def add(self):
		x = input('input x:').strip()
		print('\n')
		y = input('input y:').strip()
		print('\n')
		print('the result is ', int(x)+int(y))

	def terminal_get(self,cmd_input):
		import subprocess
		import platform
		# obj = subprocess.Popen('python E:/aa.py', shell=True, cwd='C:/', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		obj = subprocess.Popen(cmd_input, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# obj.stdin.write(b'1\n')
		# obj.stdin.write(b'2\n')
		# obj.stdin.close()
		platsys = platform.system()
		if platsys == 'Linux':
			cmd_out = str(obj.stdout.read(), 'utf-8')
		elif platsys == 'Windows':
			cmd_out = str(obj.stdout.read(), 'gbk')
		obj.stdout.close()
		return cmd_out

	def terminal_notget(self,cmd_input):
		import os
		os.system(cmd_input)

if __name__=='__main__':
	a=TerminalDeal().terminal_get('ls')
	TerminalDeal().terminal_notget("pwd")
	print(a)