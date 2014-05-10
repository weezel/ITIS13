#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import sys
import urllib

from Person import Person

verbose = 0
persons = list()


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
        tmp = runame.split(",")[0]
        runame = "".join(tmp)
    if runame.find("(") > 0:
        runame = runame.split(" (")[0]
    # italic etc html scrab
    if runame.find(">") > 0:
        runame = runame[runame.find(">") + 1: len(runame)]
    if runame.find("<") > 0:
        runame = runame[0 : runame.find(";")]
    if runame.find(";") > 0:
        runame = runame[0 : runame.find(";")]

    return runame

def decodename(url):
    return urllib.unquote(url).decode("utf-8").encode("utf-8")

def main():
    listofnames = list()
    i = 0

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

        # Clean english name too
        e = name.find("(") - 1
        if e <= 0:
            e = len(name)
        name = name[0 : e]
        name = decodename(name)
        runame = parseRuLang(r.content)


        if runame == None:
            continue

        person = Person(name, runame, wikipage)
        persons.append(person)

        i += 1
        sys.stdout.write("\r%4d / %3d\r" % (i, len(listofnames)))
        sys.stdout.flush()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\nCTRL-C pressed"

