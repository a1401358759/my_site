#!/usr/bin/env python
# -*- coding:utf-8 -*-
import oss2
from uuid import uuid4
from utils.libs.logger.syslogger import SysLogger


class AliyunOssApi(object):
    ENDPOINT_REGION_MAP = {
        "oss-cn-hangzhou.aliyuncs.com": "img-cn-hangzhou.aliyuncs.com",
        "oss-cn-qingdao.aliyuncs.com": "img-cn-qingdao.aliyuncs.com",
        "oss-cn-beijing.aliyuncs.com": "img-cn-beijing.aliyuncs.com",
        "oss-cn-shenzhen.aliyuncs.com": "img-cn-shenzhen.aliyuncs.com",
        "oss-cn-shanghai.aliyuncs.com": "img-cn-shanghai.aliyuncs.com",
        "oss-cn-hongkong.aliyuncs.com": "img-cn-hongkong.aliyuncs.com",
        "oss-us-west-1.aliyuncs.com": "img-us-west-1.aliyuncs.com",
        "oss-ap-southeast-1.aliyuncs.com": "img-ap-southeast-1.aliyuncs.com",
    }

    def __init__(self, accesskey_id=None, secret=None, endpoint=None, bucket_name=None):
        auth = oss2.Auth(accesskey_id, secret)
        # 设置超时时间
        oss2.Service(auth, endpoint, connect_timeout=30)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)

    def _gen_filename(self, filename, dirs='', path='', prefix='', name='', suffix=''):
        """
        生成OSS文件名
        :param filename:
        :param dirs:
        :param path:
        :param name:
        :param suffix:
        :return:
        """
        return "{dirs}/{path}/{prefix}{name}.{suffix}".format(
            dirs=dirs,
            path=path,
            prefix=prefix,
            name=uuid4().get_hex() if not name else name,
            suffix=filename.split('.')[-1] if not suffix else suffix
        )

    def upload_file(self, filestream=None, dirs='', path='', prefix='', name='', suffix=''):
        '''上传文件
        :params dirs: 分类目录 eg：account
        :params path: eg：user_avatar
        :param prefix: 前缀
        :params name: 文件名
        :pramas suffix: 文件后缀

        返回值：
        oss_object -- oss对象
        filename -- 文件路径
        '''
        if not filestream:
            return None, None
        filename = self._gen_filename(filestream.name, dirs=dirs, path=path, prefix=prefix, name=name, suffix=suffix)
        try:
            oss_object = self.bucket.put_object(filename, filestream)
        except Exception, exp:
            SysLogger.exception(exp)
            return None, None

        if oss_object.status != 200:
            return None, None
        else:
            return oss_object, filename

    def download_file(self, filename, target_path):
        """
        从oss下载指定文件到指定目录
        :param filename: 文件名
        :param target_path: 存储目标目录
        :return: 是否成功
        """
        try:
            self.bucket.get_object_to_file(filename, target_path)
            return True
        except Exception, exp:
            SysLogger.exception(exp)
            return False

    def sign_url(self, filename, without_sign=False, expires=5 * 60, img_host=False):
        """
        格式化网址,如果要下载文件,或提供文件下载链接,使用这个函数,会自动生成一个aliyunoss的url

        注意：可能需要发送网络请求

        :param filename: 文件名
        :param without_sign: 因为True时也要发网络请求，此参数已经废弃，留在这里是为了兼容以前的代码。False时要发请求，True时不发请求
        :param img_host: 是否转为img的host,从而可以进行图片处理
        :return:
        """
        if not filename:
            return ''
        if without_sign:
            url = self.make_url(filename)  # 不用发请求
        else:
            url = self.bucket.sign_url('GET', filename, expires)
        if img_host:
            region = self.bucket.endpoint.replace('https://', '').replace('http://', '')    # 获取当前的endpoint
            img_host = self.ENDPOINT_REGION_MAP.get(region)                                 # 获取对应的图片endpoint
            if img_host:
                return url.replace(region, img_host, 1).replace('https://', 'http://', 1)   # 进行替换,img的host不支持https
        return url

    def make_url(self, filename):
        '''
        获得完整oss资源网址

        直接拼接，不用发网络请求

        :param filename: 文件全路径名
        :return: 完整oss资源网址
        '''
        if not filename:
            return ''
        return self.bucket._make_url(self.bucket.bucket_name, filename)

    def copy_file(self, old_filename, dirs='', path='', prefix='', name='', suffix='', delete_old=True):
        """
        同一个bucket中复制文件
        :param delete_old: 是否删除旧的文件
        :return:
        """
        try:
            filename = self._gen_filename(old_filename, dirs=dirs, path=path, prefix=prefix, name=name, suffix=suffix)
            self.bucket.copy_object(self.bucket.bucket_name, old_filename, filename)
            if delete_old:
                self.bucket.delete_object(old_filename)
            return filename
        except Exception, exp:
            SysLogger.exception(exp)
            return None

    def delete_file(self, filename):
        """
        同一个bucket中删除单个文件
        :param filename: 文件短路径
        :return:
        """
        if not filename:
            return False
        try:
            self.bucket.delete_object(filename)
            return True
        except Exception, exp:
            SysLogger.exception(exp)
            return None

    def batch_delete_files(self, filename_list):
        """
        同一个bucket中删除多个文件
        :param filename_list: 文件短路径列表
        :return:
        """
        if not filename_list:
            return False
        try:
            self.bucket.batch_delete_objects(filename_list)
            return True
        except Exception, exp:
            SysLogger.exception(exp)
            return None
