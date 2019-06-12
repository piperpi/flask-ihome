# -*- coding: UTF-8 -*-

from ihome import constants
from CCPRestSDK import REST

# import ConfigParser


# 主帐号
accountSid = constants.YTX_ACCOUNT_SID

# 主帐号Token
accountToken = constants.YTX_ACCOUNT_TOKEN

# 应用Id
appId = constants.YTX_APP_ID

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com';

# 请求端口
serverPort = '8883';

# REST版本号
softVersion = '2013-12-26';


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    # for k,v in result.iteritems():
    #
    #     if k=='templateSMS' :
    #             for k,s in v.iteritems():
    #                 print '%s:%s' % (k, s)
    #     else:
    #         print '%s:%s' % (k, v)
    if result.get('statusCode') == '000000':
        return True
    else:
        return False

# sendTemplateSMS(手机号码,[验证码,分钟],1) 返回True则发送成功
# sendTemplateSMS(手机号码,内容数据,模板Id)
