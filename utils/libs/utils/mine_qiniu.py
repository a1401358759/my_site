# -*- coding: utf-8 -*-

from uuid import uuid4
from qiniu import Auth, put_data


# 需要填写你的 Access Key 和 Secret Key
access_key = 'D5m1nrbqTRDIQ1OdpeOM5eN8BL9X3KeLI6b7bwAF'
secret_key = 'VPLtQM3lwp9arR8qMeVSFKelQWO2tXpeC_yLAdo5'
domain_prefix = 'https://img.yangsihan.com/'


def upload_data(filestream, bucket_name):
    # 生成上传凭证
    q = Auth(access_key, secret_key)
    suffix = filestream.name.split('.')[-1]  # 后缀(jpg, png, gif)

    filename = uuid4().get_hex() + '.' + suffix.lower()
    token = q.upload_token(bucket_name, filename)
    # 上传文件
    retData, respInfo = put_data(token, filename, filestream)

    return filename, domain_prefix + filename
