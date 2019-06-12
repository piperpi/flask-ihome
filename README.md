## 项目简介
- flask项目  
- 前后端分离
- 第三方服务
    - [云通讯](https://www.yuntongxun.com/)短信服务(短信验证码)
    - [阿里云oss](https://www.aliyun.com/product/oss)图片服务(用户、房屋图片)
    - [支付宝](https://openhome.alipay.com/platform/home.htm)手机网站支付服务
- 功能(详见需求文档)
    - 主页
    - 注册
	- 登陆
	- 房屋列表页
	- 房屋详情页
	- 房屋预定
	- 我的爱家
	- 个人信息修改
	- 我的订单（房客）
	- 实名认证
	- 我的房源
	- 发布新房源
	- 客户订单（房东）
	- 退出    
## 项目初始化
#### 安装依赖包(运行环境python2.7)  
`pip install -r requirement.txt`
#### 配置redis缓存、mysql数据库（config.py）
```python
# 数据库
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://ihome_user:ihome_password@10.0.0.7:3306/ihome"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# redis
REDIS_HOST = "10.0.0.7"
REDIS_PORT = 6379
REDIS_PASSWORD = "redispass"
```
#### 配置celery（ihome>tasks>config.py）(异步发送短信验证码)

```python
BROKER_URL = 'redis://:redispass@10.0.0.7:6379/1'
CELERY_RESULT_BACKEND = 'redis://:redispass@10.0.0.7:6379/2'
```
#### 配置第三方服务(ihome>constants.py)
```python
# 支付宝发起请求的应用ID
ALIPAY_APPID = 'xxx'

# 阿里云oss相关信息
# 阿里云主账号AccessKey
ALIYUN_OSS_AccessKey_ID = 'xxx'
ALIYUN_OSS_AccessKeySecret = 'xxx'
# Endpoint上海为例，其它Region请按实际情况填写。
ALIYUN_OSS_ENDPOINT = 'shanghai'
# bucket_name
ALIYUN_OSS_BUCKET_NAME = 'xxx'

# 云通讯相关信息
# 主帐号
YTX_ACCOUNT_SID = 'xxx'
# 主帐号Token
YTX_ACCOUNT_TOKEN = 'xxx'
# 应用Id
YTX_APP_ID = 'xxx'
```
#### 下载支付宝公钥、应用私钥  
ihome>api_1_0>keys>**alipay_public_key.pem**  **app_private_key.pem**
```shell
openssl
OpenSSL> genrsa -out app_private_key.pem   2048  # 私钥
OpenSSL> rsa -in app_private_key.pem -pubout -out app_public_key.pem # 导出公钥
OpenSSL> exit
```
#### 启动mysql、redis、celery
```bash
systemctl start mariadb
systemctl start redis
celery -A ihome.tasks.main worker -l info
```
#### 启动flask
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

python manage.py runserver
```
