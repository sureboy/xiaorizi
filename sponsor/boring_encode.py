#! -*- coding:utf-8 -*-
#本模块用于混淆url中各id之间的规律性
#encode : int id -> string mess
#decode : string mess -> int id
#date : 2015.1.31
#author : sooshian
import base64


def encode(number, length):

    def fill(number, length):
        rawstr = str(number)
        need_num = length - len(rawstr)
        prepared = "0" * need_num + rawstr[:length]
        return prepared

    z = base64.b64encode(fill(number, length))
    result = ""
    for c in z:
        result += fill(ord(c), 3)
    return result


def decode(string):
    length = len(string)/3
    z = ""
    try:
        for i in range(length):
            z += chr(int(string[3 * i:3 * (i+1)]))
    except ValueError:
        return 0

    try:
        result = int(base64.b64decode(z))
    except TypeError:
        result = 0
    except ValueError:
        result = 0

    return result


if __name__ == "__main__":
    r = encode(1, 6)
    print r
    print decode(r)
