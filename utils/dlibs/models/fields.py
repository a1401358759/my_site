# -*- coding: utf-8  -*-
from django.db import models


class VarBinaryField(models.CharField):
    def __init__(self, *args, **kwargs):
        # max_length代表最长几个字符，这里再转成对应最长 byte
        self.max_length = kwargs['max_length']
        super(VarBinaryField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        """创建时对应的mysql字段类型

        因为utf-8一个字符占3-4个字节，所以按照最长的来，乘以4
        """
        return 'varbinary(%s)' % (self.max_length * 4)
