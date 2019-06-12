# -*- coding: utf-8 -*-
import hashlib
import oss2
from ihome import constants
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth(constants.ALIYUN_OSS_AccessKey_ID,constants.ALIYUN_OSS_AccessKeySecret )
# Endpoint以杭州为例，其它Region请按实际情况填写。
endpoint = constants.ALIYUN_OSS_ENDPOINT
bucket_name = constants.ALIYUN_OSS_BUCKET_NAME
bucket = oss2.Bucket(auth, 'http://oss-cn-%s.aliyuncs.com' % endpoint, bucket_name)


# 必须以二进制的方式打开文件，因为需要知道文件包含的字节数。
# with open('./2.png', 'rb') as fileobj:
#     # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
#     # fileobj.seek(1000, os.SEEK_SET)
#     # # Tell方法用于返回当前位置。
#     # current = fileobj.tell()
#     bucket.put_object(None, fileobj)
def img_store(data, format=None):
    filename = hashlib.sha1(data).hexdigest()
    if format:
        filename = filename + '.' + format
    res = bucket.put_object(filename, data)
    if res.status == 200:
        img_url = 'https://%s.oss-cn-%s.aliyuncs.com/%s' % (bucket_name, endpoint, filename)
        return img_url
    else:
        return None


if __name__ == '__main__':
    with open('./1.jpg', 'rb') as f:
        data = f.read()
        url = img_store(data, 'jpg')
        print(url)