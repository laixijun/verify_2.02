import logging
import os

import logging.handlers

# from config import basedir3
#
# log_file=os.path.join(basedir3,'testfile/log/access.log')
logger = logging.getLogger() #定义对应的程序模块名name，默认是root
logger.setLevel(logging.DEBUG) #指定最低的日志级别

ch = logging.StreamHandler() #日志输出到屏幕控制台
ch.setLevel(logging.DEBUG) #设置日志等级

# fh = logging.FileHandler(filename='access.log',encoding='utf-8')#向文件access.log输出日志信息
curPath = os.path.abspath(os.path.dirname(__file__))
filename=os.path.join(curPath,'myapp.log')
fh = logging.handlers.RotatingFileHandler(filename=filename, mode='a', maxBytes=102400, backupCount=10, encoding='utf-8')
fh.setLevel(logging.DEBUG) #设置输出到文件最低日志级别

#create formatter
formatter = logging.Formatter('%(asctime)s %(pathname)s [line:%(lineno)d] %(message)s',datefmt="%Y-%m-%d %H:%M:%S") #定义日志输出格式

#add formatter to ch and fh
ch.setFormatter(formatter) #选择一个格式
fh.setFormatter(formatter)

logger.addHandler(ch) #增加指定的handler
logger.addHandler(fh)

# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')
# print(log_file)


if __name__=='__main__':
	pass