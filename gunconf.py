def test01():
	import gevent.monkey
	import multiprocessing

	gevent.monkey.patch_all()

	# 监听本机的5000端口
	bind = '0.0.0.0:5000'
	#nginx listen       8088;
	preload_app = True

	# 开启进程
	# workers=4
	workers = multiprocessing.cpu_count() * 2 + 1

	# 每个进程的开启线程
	threads = multiprocessing.cpu_count() * 2

	backlog = 2048

	# 工作模式为gevent
	worker_class = "gevent"

	# debug=True

	# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
	daemon = True

	# 进程名称
	proc_name = 'gunicorn.pid'

	# 进程pid记录文件
	pidfile = 'app_pid.log'

	loglevel = 'debug'
	logfile = 'debug.log'
	accesslog = 'access.log'
	access_log_format = '%(h)s %(t)s %(U)s %(q)s'
	errorlog = "error.log"

import os
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

debug = False
# 设置守护进程【关闭连接时，程序仍在运行】
daemon = True
# daemon = False
loglevel = 'debug'
bind = '0.0.0.0:5000'
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'

#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
x_forwarded_for_header = 'X-FORWARDED-FOR'
