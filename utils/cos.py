# -*- coding: utf-8 -*-

# 腾讯cos账号
TencentCosConf = {
    "app_id": "1256044091",
    "secret_id": "AKIDCf6dHrjkdXDwYCtbN9rVzNj1f0KTgZeg",
    "secret_key": "9DXEc9cu28A0Ur6G0gCY9ZDl7IXqBMME",
    "region": "ap-beijing",
}

from httplib2 import Http
import random
import time
import urllib
import hmac
import hashlib
import binascii
import base64
import requests
import os


class Cos:
    def __init__(self, app_id, secret_id, secret_key, region="shanghai"):
        self.config = CosConfig()
        self.config.app_id = int(app_id)
        self.config.secret_id = secret_id
        self.config.secret_key = secret_key
        self.config.region = region

    def get_bucket(self, bucket_name):
        return CosBucket(self.config, bucket_name)


class CosConfig:
    app_id = 0
    secret_id = ''
    secret_key = ''
    region = ''
    bucket = ''


class CosBucket:

    def __init__(self, cos_config, bucket_name):
        """
        初始化操作
        """
        self.config = cos_config
        self.config.bucket = bucket_name
        self.http = Http()
        self.headers = {'Content-Type': 'application/json'}

    def create_folder(self, dir_name):
        """创建目录(https://www.qcloud.com/document/product/436/6061)
        :param dir_name:要创建的目录的目录的名称
        :return 返回True创建成功，返回False创建失败
        """
        if dir_name[0] == '/':
            dir_name = dir_name[1:len(dir_name)]
        self.url = "http://<Region>.file.myqcloud.com" + "/files/v2/<appid>/<bucket_name>/<dir_name>/"
        self.url = self.url.replace("<Region>", self.config.region).replace("<appid>", str(self.config.app_id))
        self.url = str(self.url).replace("<bucket_name>", self.config.bucket).replace("<dir_name>", dir_name)
        self.headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        response, content = self.http.request(uri=self.url, method='POST', body='{"op": "create", "biz_attr": ""}', headers=self.headers)
        if eval(content.decode('utf8')).get("code") == 0:
            return True
        else:
            return False

    def list_folder(self, dir_name=None, prefix=None, num=1000, context=None):
        """列目录(https://www.qcloud.com/document/product/436/6062)
        :param dir_name:文件夹名称
        :param prefix:前缀
        :param num:查询的文件的数量，最大支持1000，默认查询数量为1000
        :param context:翻页标志，将上次查询结果的context的字段传入，即可实现翻页的功能
        :return 查询结果，为json格式
        """
        if dir_name[0] == '/':
            dir_name = dir_name[1:len(dir_name)]
        self.url = 'http://<Region>.file.myqcloud.com/files/v2/<appid>/<bucket_name>/'
        self.url = self.url.replace("<Region>", self.config.region).replace("<appid>", str(self.config.app_id)).replace("<bucket_name>", self.config.bucket)
        if dir_name is not None:
            self.url = self.url + str(dir_name) + "/"
        if prefix is not None:
            self.url = self.url + str(prefix)
        self.url = self.url + "?op=list&num=" + str(num)
        if context is not None:
            self.url = self.url + '&context=' + str(context)
        self.headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        response, content = self.http.request(uri=self.url, method='GET', headers=self.headers)
        return content.decode("utf8")

    def query_folder(self, dir_name):
        """查询目录属性(https://www.qcloud.com/document/product/436/6063)
        :param dir_name:查询的目录的名称
        :return:查询出来的结果，为json格式
        """
        if dir_name[0] == '/':
            dir_name = dir_name[1:len(dir_name)]
        self.url = 'http://' + self.config.region + '.file.myqcloud.com' + '/files/v2/' + str(self.config.app_id) + '/' + self.config.bucket + '/' + dir_name + '/?op=stat'
        self.headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        reponse, content = self.http.request(uri=self.url, method='GET', headers=self.headers)
        return content.decode("utf8")

    def delete_folder(self, dir_name):
        """删除目录
        :param dir_name:删除的目录的目录名
        :return: 删除结果，成功返回True，失败返回False
        """
        if dir_name[0] == '/':
            dir_name = dir_name[1:len(dir_name)]
        self.url = 'http://' + self.config.region + '.file.myqcloud.com/files/v2/' + str(self.config.app_id) + '/' + self.config.bucket + '/' + dir_name + '/'
        self.headers['Authorization'] = CosAuth(self.config).sign_once(self.config.bucket, dir_name + '/')
        response, content = self.http.request(uri=self.url, method='POST', body='{"op": "delete"}', headers=self.headers)
        if eval(content.decode('utf8')).get('code') == 0:
            return True
        else:
            return False

    def upload_file(self, real_file_path, file_name, dir_name=None):
        """简单上传文件(https://www.qcloud.com/document/product/436/6066)
        :param real_file_path: 文件的物理地址
        :param file_name: 文件名称
        :param dir_name: 文件夹名称（可选）
        :return:json数据串
        """

        if dir_name is not None and dir_name[0] == '/':
            dir_name = dir_name[1:len(dir_name)]
        if dir_name is None:
            dir_name = ""
        self.url = 'http://' + self.config.region + '.file.myqcloud.com/files/v2/' + str(self.config.app_id) + '/' + self.config.bucket
        if dir_name is not None:
            self.url = self.url + '/' + dir_name
        self.url = self.url + '/' + file_name
        headers = {}
        headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        # files = {'file': ('', open(real_file_path, 'rb'))}
        r = requests.post(url=self.url, data={'op': 'upload', 'biz_attr': '', 'insertOnly': '0'}, files={
            'filecontent': (real_file_path, open(real_file_path, 'rb'), 'application/octet-stream')}, headers=headers)
        return str(eval(r.content.decode('utf8')).get('data'))

    def _upload_slice_control(self, file_size, slice_size):
        headers = {}
        headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        data = {'op': 'upload_slice_init', 'filesize': str(file_size), 'slice_size': str(slice_size), 'biz_attr': '',
                'insertOnly': '0'}
        r = requests.post(url=self.url, files=data, headers=headers)
        return str(eval(r.content.decode('utf8')).get('data').get('session'))

    def _upload_slice_data(self, filecontent, session, offset):
        headers = {}
        headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        data = {'op': 'upload_slice_data', 'filecontent': filecontent, 'session': session, 'offset': str(offset)}
        r = requests.post(url=self.url, files=data, headers=headers)
        return str(eval(r.content.decode('utf8')).get('data'))

    def _upload_slice_finish(self, session, file_size):
        headers = {}
        headers['Authorization'] = CosAuth(self.config).sign_more(self.config.bucket, '', 30)
        data = {'op': 'upload_slice_finish', 'session': session, 'filesize': str(file_size)}
        r = requests.post(url=self.url, files=data, headers=headers)
        return str(eval(r.content.decode('utf8')).get('data'))

    def upload_slice_file(self, real_file_path, slice_size, file_name, offset=0, dir_name=None):
        """
        此分片上传代码由GitHub用户a270443177(https://github.com/a270443177)友情提供
        :param real_file_path:
        :param slice_size:
        :param file_name:
        :param offset:
        :param dir_name:
        :return:
        """
        if dir_name is not None and dir_name[0] == '/':
            dir_name = dir_name[1:len(dir_name)]
        if dir_name is None:
            dir_name = ""
        self.url = 'http://' + self.config.region + '.file.myqcloud.com/files/v2/' + str(
            self.config.app_id) + '/' + self.config.bucket
        if dir_name is not None:
            self.url = self.url + '/' + dir_name
        self.url = self.url + '/' + file_name
        file_size = os.path.getsize(real_file_path)
        session = self._upload_slice_control(file_size=file_size, slice_size=slice_size)
        with open(real_file_path, 'rb') as local_file:
            while offset < file_size:
                file_content = local_file.read(slice_size)
                self._upload_slice_data(filecontent=file_content, session=session, offset=offset)
                offset += slice_size
            r = self._upload_slice_finish(session=session, file_size=file_size)
        return r

    def move_file(self, source_fileid, dest_fileid):
        """"""
        source_fileid = source_fileid.replace("\\", '/')
        dest_fileid = dest_fileid.replace("\\", "/")
        if source_fileid[0] == '/':
            source_fileid = source_fileid[1:len(source_fileid)]
        self.url = "http://" + self.config.region + ".file.myqcloud.com/files/v2/" + str(self.config.app_id) + "/" + self.config.bucket + "/" + source_fileid
        headers = {}
        headers['Authorization'] = CosAuth(self.config).sign_once(self.config.bucket, source_fileid)
        r = requests.post(url=self.url, data={'op': 'move', 'dest_fileid': dest_fileid, 'to_over_write': '0'}, files={'filecontent': ('', '', 'application/octet-stream')}, headers=headers)
        code = eval(r.content.decode('utf8')).get('code')
        if code == 0:
            return True
        else:
            return False

    def copy_file(self, source_fileid, dest_fileid):
        """"""
        source_fileid = source_fileid.replace("\\", '/')
        dest_fileid = dest_fileid.replace("\\", "/")
        if source_fileid[0] == '/':
            source_fileid = source_fileid[1:len(source_fileid)]
        self.url = "http://" + self.config.region + ".file.myqcloud.com/files/v2/" + str(self.config.app_id) + "/" + self.config.bucket + "/" + source_fileid
        headers = {}
        headers['Authorization'] = CosAuth(self.config).sign_once(self.config.bucket, source_fileid)
        r = requests.post(url=self.url, data={'op': 'copy', 'dest_fileid': dest_fileid, 'to_over_write': '0'}, files={'filecontent': ('', '', 'application/octet-stream')}, headers=headers)
        code = eval(r.content.decode('utf8')).get('code')
        if code == 0:
            return True
        else:
            return False

    def delete_file(self, dest_fileid):
        """
        """
        dest_fileid = dest_fileid.replace("\\", "/")
        if dest_fileid[0] == '/':
            dest_fileid = dest_fileid[1:len(dest_fileid)]
        self.url = "http://" + self.config.region + ".file.myqcloud.com/files/v2/" + str(
            self.config.app_id) + "/" + self.config.bucket + "/" + dest_fileid
        self.headers['Authorization'] = CosAuth(self.config).sign_once(self.config.bucket, dest_fileid)
        response, content = self.http.request(uri=self.url, method='POST', body='{"op": "delete"}',
                                              headers=self.headers)
        code = eval(content.decode('utf8')).get('code')
        if code == 0:
            return True
        else:
            return False

    def upload_file_from_url(self, url, file_name, dir_name=None):
        """简单上传文件(https://www.qcloud.com/document/product/436/6066)
        :param url: 文件url地址
        :param file_name: 文件名称
        :param dir_name: 文件夹名称（可选）
        :return:json数据串
        """
        real_file_name = str(int(time.time() * 1000))
        urllib.request.urlretrieve(url, real_file_name)
        data = self.upload_file(real_file_name, file_name, dir_name)
        os.remove(real_file_name)
        return data


class CosAuth(object):
    def __init__(self, config):
        self.config = config

    def app_sign(self, bucket, cos_path, expired, upload_sign=True):
        appid = self.config.app_id
        bucket = bucket
        secret_id = self.config.secret_id
        now = int(time.time())
        rdm = random.randint(0, 999999999)
        cos_path = urllib.quote(cos_path.encode('utf8'), '~/')  # urllib.parse.quote  python3
        if upload_sign:
            fileid = '/%s/%s/%s' % (appid, bucket, cos_path)
        else:
            fileid = cos_path

        if expired != 0 and expired < now:
            expired = now + expired

        sign_tuple = (appid, secret_id, expired, now, rdm, fileid, bucket)

        plain_text = 'a=%s&k=%s&e=%d&t=%d&r=%d&f=%s&b=%s' % sign_tuple
        secret_key = self.config.secret_key.encode('utf8')
        sha1_hmac = hmac.new(secret_key, plain_text.encode("utf8"), hashlib.sha1)
        hmac_digest = sha1_hmac.hexdigest()
        hmac_digest = binascii.unhexlify(hmac_digest)
        sign_hex = hmac_digest + plain_text.encode('utf8')
        sign_base64 = base64.b64encode(sign_hex)
        return sign_base64.decode('utf8')

    def sign_once(self, bucket, cos_path):
        """单次签名(针对删除和更新操作)
        :param bucket: bucket名称
        :param cos_path: 要操作的cos路径, 以'/'开始
        :return: 签名字符串
        """
        return self.app_sign(bucket, cos_path, 0)

    def sign_more(self, bucket, cos_path, expired):
        """多次签名(针对上传文件，创建目录, 获取文件目录属性, 拉取目录列表)
        :param bucket: bucket名称
        :param cos_path: 要操作的cos路径, 以'/'开始
        :param expired: 签名过期时间, UNIX时间戳, 如想让签名在30秒后过期, 即可将expired设成当前时间加上30秒
        :return: 签名字符串
        """
        return self.app_sign(bucket, cos_path, expired)

    def sign_download(self, bucket, cos_path, expired):
        """下载签名(用于获取后拼接成下载链接，下载私有bucket的文件)
        :param bucket: bucket名称
        :param cos_path: 要下载的cos文件路径, 以'/'开始
        :param expired:  签名过期时间, UNIX时间戳, 如想让签名在30秒后过期, 即可将expired设成当前时间加上30秒
        :return: 签名字符串
        """
        return self.app_sign(bucket, cos_path, expired, False)
