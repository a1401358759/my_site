# -*- coding: utf-8 -*-

import random
# import time
from qiniu import Auth, put_data


# 需要填写你的 Access Key 和 Secret Key
access_key = 'D5m1nrbqTRDIQ1OdpeOM5eN8BL9X3KeLI6b7bwAF'
secret_key = 'VPLtQM3lwp9arR8qMeVSFKelQWO2tXpeC_yLAdo5'
# bucket_name = 'blog'
domain_prefix = 'http://img.yangsihan.com/'


def upload_data(data, bucket_name):
    # 生成上传凭证
    q = Auth(access_key, secret_key)
    key = ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz', 8)) + '.png'
    token = q.upload_token(bucket_name, key)
    # 上传文件
    retData, respInfo = put_data(token, key, data)

    return key, domain_prefix + key + '-watermark'
