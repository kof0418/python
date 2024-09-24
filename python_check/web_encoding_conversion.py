#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018/08/13

import os
import sys
import re
import codecs
import chardet

EXTENSIONS = (".php", ".htm", ".html", ".dwt", ".sql")
FROM_ENCODING = "big5"
TO_ENCODING = "utf-8"


def get_encoding(fn):
    raw_file = open(fn, "rb")
    encoding = chardet.detect(raw_file.read())["encoding"]
    raw_file.close()

    return encoding


def do_conversion(fn, encoding):
    if encoding == None:
        encoding = FROM_ENCODING

    input_file = codecs.open(fn, "r", encoding, errors="ignore")
    content = input_file.read()
    input_file.close()

    encoding_insensitive = re.compile(re.escape(FROM_ENCODING), re.I)
    content = content.replace(FROM_ENCODING, TO_ENCODING)
    content = encoding_insensitive.sub(TO_ENCODING, content)

    output_file = codecs.open(fn, "w", TO_ENCODING)
    output_file.write(content)
    output_file.close()


def web_encoding_conversion():
    total = 0
    converted = 0

    if len(sys.argv) >= 2:
        input_path = os.path.expanduser(sys.argv[1])

        for dirname, dirnames, filenames in os.walk(input_path):
            for fn in filenames:
                if fn.lower().endswith(EXTENSIONS):
                    total = total + 1
                    full_path = os.path.join(dirname, fn)
                    encoding = get_encoding(full_path)
                    print("{0} - {1}".format(encoding, full_path))
                    do_conversion(full_path, encoding)
                    converted = converted + 1

    print("{0} files checked, {1} converted.".format(total, converted))


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    web_encoding_conversion()
