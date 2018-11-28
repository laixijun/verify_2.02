from flask import url_for,redirect,session
from functools import wraps

def is_login(func):
    """
    定义登录注册验证的装饰器
    :return: check_login
    """
    @wraps(func)
    def check_login(*args,**kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('user.login'))
    return check_login
