#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
修改历史
1. 2014-10-15 -- peng.zhao 修改padding方式
2. 2014-10-17 -- peng.zhao 增加二进制加解密支持

"""


def pad(s):
    '''padding规则: 缺x就补x个,例外情况是缺0个补4个

    字符串末位补 '\0'
    '''
    s += chr(0)  # 兼容c版末尾补'\0'
    padding_len = 4 - (len(s) % 4)
    s += chr(padding_len) * padding_len
    return s


def pad_bin(byte_list):
    '''padding规则: 缺x就补x个,例外情况是缺0个补4个

    bin 末位不补
    '''
    padding_len = 4 - (len(byte_list) % 4)
    byte_list.extend([chr(padding_len)] * padding_len)
    return byte_list


def unpad(s):
    unpadding_len = 0
    for i in xrange(len(s)):
        if s[:-1 - i] != 0:
            unpadding_len = s[-1 - i] + i
            break
    return s[:-unpadding_len]


def str2longs(s):
    length = (len(s) + 3) / 4
    s = s.ljust(length * 4, '\0')
    result = []
    for i in xrange(length):
        j = 0
        j |= ord(s[i * 4])
        j |= ord(s[i * 4 + 1]) << 8
        j |= ord(s[i * 4 + 2]) << 16
        j |= ord(s[i * 4 + 3]) << 24
        result.append(j)
    return result


def longs2str(s):
    result_list = []
    for c in s:
        result_list.append(chr(c & 0xFF) + chr(c >> 8 & 0xFF)
                           + chr(c >> 16 & 0xFF) + chr(c >> 24 & 0xFF))
    result = ''.join(result_list)
    return result.rstrip('\0')


def bytes2longs(s):
    length = len(s) / 4
    result = []
    for i in xrange(length):
        j = 0
        j |= ord(s[i * 4])
        j |= ord(s[i * 4 + 1]) << 8
        j |= ord(s[i * 4 + 2]) << 16
        j |= ord(s[i * 4 + 3]) << 24
        result.append(j)
    return result


def longs2bytes(s):
    result_list = []
    for c in s:
        result_list.append(c & 0xFF)
        result_list.append(c >> 8 & 0xFF)
        result_list.append(c >> 16 & 0xFF)
        result_list.append(c >> 24 & 0xFF)
    return result_list


def btea(v, n, k):
    if not isinstance(v, list) or \
            not isinstance(n, int) or \
            not isinstance(k, (list, tuple)):
        return False

    MX = lambda: ((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4)) ^ (sum ^ y) + (k[(p & 3) ^ e] ^ z)
    u32 = lambda x: x & 0xffffffff

    y = v[0]
    sum = 0
    DELTA = 0x9e3779b9
    if n > 1:
        z = v[n - 1]
        q = 6 + 52 / n
        while q > 0:
            q -= 1
            sum = u32(sum + DELTA)
            e = u32(sum >> 2) & 3
            p = 0
            while p < n - 1:
                y = v[p + 1]
                z = v[p] = u32(v[p] + MX())
                p += 1
            y = v[0]
            z = v[n - 1] = u32(v[n - 1] + MX())
        return True
    elif n < -1:
        n = -n
        q = 6 + 52 / n
        sum = u32(q * DELTA)
        while sum != 0:
            e = u32(sum >> 2) & 3
            p = n - 1
            while p > 0:
                z = v[p - 1]
                y = v[p] = u32(v[p] - MX())
                p -= 1
            z = v[n - 1]
            y = v[0] = u32(v[0] - MX())
            sum = u32(sum - DELTA)
        return True
    return False


def encrypt(plain, key):
    key = key.ljust(16, '\0')
    k = str2longs(key)
    # 填充
    plain = pad(plain)
    v = str2longs(plain)
    n = len(v)
    btea(v, n, k)

    result = longs2str(v)
    return result


def encrypt_bin(byte_array, key):
    '''未实现,目前不可用'''
    key = key.ljust(16, '\0')
    k = str2longs(key)
    # 填充
    bytes_list = pad_bin(list(byte_array))
    v = str2longs(str(bytes_list))
    n = len(v)
    btea(v, n, k)

    result = longs2str(v)
    return result


def decrypt(s, key):
    key = key.ljust(16, '\0')
    k = str2longs(key)
    v = str2longs(s)
    n = len(v)
    btea(v, -n, k)

    v = longs2bytes(v)
    return unpad(v)


if __name__ == '__main__':
    key = "hey, lyxint"
    s = "what's up, dude??"
    enc = encrypt(s, key, False)
    print len(enc), enc
    dec = decrypt(enc, key, False)
    print len(dec), dec
    assert s == dec