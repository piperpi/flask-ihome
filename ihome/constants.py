# coding=utf-8

# redis 存储图片验证码超时时间，单位s
REDIS_IMAGE_CODE_EXPIRES = 180

# redis 存储短信验证码有效期，单位s
SMS_CODE_REDIS_EXPIRES = 300

# redis 存储短信验证码超时时间，单位s
SEND_SMS_CODE_INTERVAL = 60

# 登录错误最大尝试次数
LOGIN_ERROR_MAX_TIMES = 3

# 登录次数超过限制禁止登录时间
LOGIN_ERROR_FORBID_TIME = 300

# redis缓存城区超时时间，单位s
AREA_INFO_REDIS_EXPIRES = 300

# 房屋订单数目最多的数据条数
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页数据容量
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面页数缓存时间，单位秒
HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES = 7200

# 支付宝手机网站支付前缀
ALIPAY_URL_PREFIX = 'https://openapi.alipaydev.com/gateway.do?'

# 支付宝发起请求的应用ID
ALIPAY_APPID = 'xxx'

# 支付宝返回的链接地址
ALIPAY_RETURN_URL = 'http://127.0.0.1:5000/payComplete.html'

# 阿里云oss相关信息
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
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
