# -*- coding: utf-8  -*-
#!/usr/local/bin/python
import csv
import codecs
import cStringIO
import os.path
from django.utils.translation import ugettext as _


class UTF8CSVRecoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeCSVReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8CSVRecoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeCSVWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoding = encoding
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode(self.encoding) for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode(self.encoding)
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        value = self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
        return value

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def ReadCSVFile(filepath, delimiter=',', encoding="gbk"):
    _name, _ext = os.path.splitext(os.path.basename(filepath))
    if not _ext or _ext.lower() != ".csv":
        raise Exception(_("只允许CSV文件！"))

    _file = None
    try:
        _file = open(filepath, 'rb')
        reader = UnicodeCSVReader(_file, dialect=csv.excel, encoding=encoding, delimiter=delimiter)
        titles = reader.next()  # read header row for csv.
        try:
            titles[0] = str(titles[0])
        except:
            titles[0] = str(titles[0][1:])

        rows = []
        while True:
            try:
                item = reader.next()  # read data row for csv
                if not item:
                    break
                row = {}
                for title in titles:
                    row[title.lower().strip()] = item[titles.index(title)]
                rows.append(row)
            except:
                break
        return rows
    finally:
        if _file:
            _file.close()
            _file = None


class Echo(object):

    def write(self, value):
        return value
