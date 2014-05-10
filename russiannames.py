#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import sys
import urllib

verbose = 0


def parseRuLang(data):
    findable = 'xml:lang="ru">'

    # Begin with <span lang
    b = data.find(findable)
    if b == -1:
        return None
    # Strip xml scrab out
    tmp = data.find(">", b)
    if tmp != -1:
        b = tmp + 1

    # ..until the closing </span>
    e = data.find("</span>", b)
    if e == -1:
        return None

    runame = data[b:e]
    if runame.find(",") > 0:
        tmp = runame.split(",")
        runame = "".join(tmp)
    if runame.find("(") > 0:
        runame = data[b:e].split(" (")[0]
    # italic etc html scrab
    if runame.find(">") > 0:
        runame = runame[runame.find(">") + 1: len(runame)]
    if runame.find("<") > 0:
        runame = runame[0 : runame.find(";")]
    if runame.find(";") > 0:
        runame = runame[0 : runame.find(";")]

    try:
        return decodeurl(runame)
    except UnicodeDecodeError:
        return decodeurl

def decodeurl(url):
    return urllib.unquote(url).decode("utf-8")

def main():
    listofnames = list()
    with open("listofrussian.txt") as f:
        listofnames = f.readlines()

    for name in listofnames:
        name = name.rstrip("\n")
        wikipage = u"http://en.wikipedia.org/wiki/%s" % name

        r = requests.get(wikipage)
        if r == None:
            print "Cannot find Russian language section for %s" % name.replace("_", " ")
            continue

        if verbose:
            print wikipage

        runame = parseRuLang(r.content)
        print "%s = %s" % (name.replace("_", " "), runame)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\nCTRL-C pressed"

