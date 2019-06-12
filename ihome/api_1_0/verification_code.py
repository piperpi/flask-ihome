# coding:utf-8
import random

from flask import current_app, jsonify, make_response, request

from ihome import redis_store, constants
from ihome.api_1_0 import api
# from ihome.libs.yuntongxun import SendTemplateSMS
from ihome.tasks.sms.tasks import send_sms
from ihome.models import User
from ihome.utils.captcha import captcha
from ihome.utils.response_code import RET


# http://127.0.0.1:5000/api/v1.0/image_codes/xxx
@api.route('/image_codes/<img_code_id>')
def get_image_codes(img_code_id):
    name, text, img_data = captcha.captcha.generate_captcha()
    try:
        redis_store.setex('img_code_%s' % img_code_id, constants.REDIS_IMAGE_CODE_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='save img faild')
    resp = make_response(img_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 校验参数
    if not all([image_code_id, image_code]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get("img_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")

    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或者过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写的值进行对比
    if real_image_code.lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后重试")

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在，则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    print('sms_code', sms_code)

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信的操作
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # celery异步发送短信
    result = send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)

    return jsonify(errno=RET.OK, errmsg="发送成功")
