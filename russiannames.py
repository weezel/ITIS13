#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import re
import requests
import sys
import urllib

from Person import Person

verbose = 0
fname_rusnames = "rusnames.dump"


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
        runame = runame[0 : runame.find("<")]
    if runame.find(";") > 0:
        runame = runame[0 : runame.find(";")]

    return runame.decode("utf-8").encode("utf-8")


def decodename(url):
    return urllib.unquote(url).decode("utf-8").encode("utf-8")


def savenames2file(names):
    """
    Save names to a file. Saves bandwidth and nerves.
    """
    pickle.dump(names, open(fname_rusnames, "wb"))


def loadnamesfromfile():
    """
    Load names from a file. Saves bandwidth and nerves.
    """
    persons = pickle.load(open(fname_rusnames, "rb"))
    return persons


def fetchnames():
    listofnames = list()
    persons = list()

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
        name = decodename(name).replace("_", " ")
        runame = parseRuLang(r.content)

        if runame == None:
            continue

        person = Person(name, runame, wikipage)
        persons.append(person)

        i += 1
        print "[%4d / %3d] %s" % (i, len(listofnames), person)
    print "\n",

    return persons


def main():
    persons = list()

    if os.path.isfile(fname_rusnames):
        persons = loadnamesfromfile()
    else:
        persons = fetchnames()
        savenames2file(persons)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\nCTRL-C pressed"

