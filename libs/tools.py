import threading

def threadingTimer(time,func):
	timer = threading.Timer(time, func)
	timer.start()