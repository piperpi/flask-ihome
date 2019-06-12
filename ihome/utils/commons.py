# coding:utf-8

import functools

from flask import session, g, jsonify
from werkzeug.routing import BaseConverter

from ihome.utils.response_code import RET


# 定义正则转换器
class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')

        if user_id:
            g.user_id = user_id
            return func(*args, **kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

    return wrapper
