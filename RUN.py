#gunicorn -c config.py(gunicorn配置文件)  flask_nginx(flask启动文件):app
from libs.terminaldeal import TerminalDeal



if __name__ == "__main__":
	TerminalDeal().terminal_notget("gunicorn -c gunconf.py manage:app")
	# TerminalDeal().terminal_notget("ls")





