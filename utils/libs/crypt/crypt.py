# -*- coding: utf-8  -*-

'''
加密、解密类库
'''

import string

from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

from .xxtea import (decrypt as xxt_decrypt,
                    encrypt as xxt_encrypt)
from utils.libs.logger import SysLogger


def random_str(length=8):
    '''生成可打印的 [0-9a-zA-Z] 随机字符串.'''
    seeds = string.letters + string.digits
    random_str = ''
    for x in xrange(length):
        random_str += random.choice(seeds)
    return random_str


def aes_encrypt(plaintext, key, iv=None, flag="raw"):
    """ AES-128bit/MODE_CBC/PKCS7Padding

    @ plaintext -- 明文
    @ key -- 密钥
    @ iv -- None时随机，[a-zA-Z0-9]

    returns:
        (cipher, iv)
    """
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (chr(x) * x)

    try:
        padded_plaintext = pad(plaintext)

        if iv is None:
            iv = random_str(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        encrypted, iv_ = cipher.encrypt(padded_plaintext.encode("utf-8")), iv

        if "base64" == flag:
            encrypted = b64encode(encrypted)

        return encrypted, iv_
    except Exception, exp:
        SysLogger.exception(exp)
        return None, ''


def aes_decrypt(ciphertext, key, iv, flag="raw"):
    """ AES-128bit/MODE_CBC/PKCS7Padding

    @ plaintext -- 密文
    @ key -- 密钥
    @ iv -- iv
    returns:
        plaintext
    """
    def unpad(s):
        return s[:-ord(s[-1])]

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        if "base64" == flag:
            ciphertext = b64decode(ciphertext)
        plaintext = unpad(cipher.decrypt(ciphertext))
        return plaintext
    except Exception, exp:
        SysLogger.exception(exp)
        return None


def aes_encrypt_base64_iv(plaintext, key):
    '''iv嵌入到密文头部，再做base64编码的aes-cbc加密'''
    try:
        iv = Random.new().read(AES.block_size)
        ciphertext = aes_encrypt(plaintext, key, iv)[0]
        return b64encode(iv + ciphertext)
    except Exception, exp:
        SysLogger.exception(exp)
        return None


def aes_decrypt_base64_iv(ciphertext, key):
    '''先做base64解码，再从密文头部截断iv后做aes-cbc解密'''
    try:
        decoded = b64decode(ciphertext)
        iv, ciphertext = decoded[:AES.block_size], decoded[AES.block_size:]
        return aes_decrypt(ciphertext, key, iv)
    except Exception, exp:
        SysLogger.exception(exp)
        return None


def xxtea_encrypt(plaintext, key, flag="base64", is_bin=False):
    try:
        if is_bin:
            pass
        else:
            cipher = xxt_encrypt(plaintext, key)
        if flag == "base64":
            cipher = b64encode(cipher)
        return cipher
    except Exception, exp:
        SysLogger.exception(exp)
        return None


def xxtea_decrypt(cipher, key, flag="base64", is_bin=False):
    try:
        if flag == "base64":
            cipher = b64decode(cipher)
            byte_list = xxt_decrypt(cipher, key)
            if is_bin:
                return bytes(bytearray(byte_list))
            else:
                return bytes(bytearray(byte_list[:-1]))  # 去掉末位的 \0
    except Exception, exp:
        SysLogger.exception(exp)
        return None
