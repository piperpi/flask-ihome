# coding:utf-8
from flask import request, jsonify, current_app, session
import re
from ihome.api_1_0 import api
from ihome.utils.response_code import RET
from ihome import redis_store, db, constants
from ihome.models import User
from sqlalchemy.exc import IntegrityError


@api.route('/users', methods=['POST'])
def register():
    try:
        req_data = request.get_json()
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg='请传入json数据')
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg='请传入json数据')
    mobile = req_data.get('mobile')
    sms_code = req_data.get('sms_code')
    password = req_data.get('password')
    password2 = req_data.get('password2')
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    elif not re.match('1\d{10}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')
    elif password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg='两次输入密码不相等')

    try:
        real_sms_code = redis_store.get('sms_code_%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis数据库错误')
    else:
        if not real_sms_code:
            return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期')
        elif real_sms_code != sms_code:
            return jsonify(errno=RET.PARAMERR, errmsg='短信验证码错误')
    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

        # 保存用户的注册数据到数据库中
    user = User(name=mobile, mobile=mobile)
    # user.generate_password_hash(password)

    user.password = password  # 设置属性

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    return jsonify(errno=RET.OK, errmsg='注册用户成功')


@api.route('/sessions', methods=['POST'])
def login():
    try:
        req_data = request.get_json()
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg='请传入json数据')
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg='请传入json数据')
    mobile = req_data.get('mobile')
    password = req_data.get('password')
    if not all([mobile, password, ]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    user_ip = request.remote_addr
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")
    try:
        user = User.query.filter_by(mobile=mobile).first()

    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if user is None or not user.check_password(password):
            # 如果验证失败，记录错误次数，返回信息
            try:
                # redis的incr可以对字符串类型的数字数据进行加一操作，如果数据一开始不存在，则会初始化为1
                redis_store.incr("access_num_%s" % user_ip)
                redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
            except Exception as e:
                current_app.logger.error(e)

            return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    print(session)

    return jsonify(errno=RET.OK, errmsg='验证完成，可以登录')

@api.route('/session', methods=['GET'])
def check_login():
    name = session.get('name')
    if name:
        return jsonify(errno=RET.OK, errmsg='用户已登录',data={'name':name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户已登录')

@api.route("/sessions", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    csrf_token = session.get('csrf_token')
    session.clear()
    session['csrf_token'] = csrf_token
    return jsonify(errno=RET.OK, errmsg="OK")