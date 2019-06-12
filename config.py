# coding:utf-8

import redis


class Config(object):
    """配置信息"""
    SECRET_KEY = "wefewewew"

    STATIC_FOLDER = '/static'

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://ihome_user:ihome_password@10.0.0.7:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "10.0.0.7"
    REDIS_PORT = 6379
    REDIS_PASSWORD = "redispass"

    # flask-session配置
    # SESSION_TYPE = "filesystem"
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位秒


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}