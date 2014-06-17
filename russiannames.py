#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import re
import requests
import sys
import urllib

from difflib import SequenceMatcher
from transliterate import translit, get_available_language_codes
from Person import Person

verbose = 0
fname_rusnames = "rusnames.dump"


def parseRuLang(data):
    findable = 'xml:lang="ru">'

    # Begin with <span lang
    b = data.find(findable)
    if b == -1:
        return None
    # Strip xml scrap out
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
    # italic etc html scrap
    if runame.find(">") > 0:
        runame = runame[runame.find(">") + 1: len(runame)]
    if runame.find("<") > 0:
        runame = runame[0 : runame.find("<")]
    if runame.find(";") > 0:
        runame = runame[0 : runame.find(";")]

    return unicode(runame, "utf-8") #.encode("utf-8")


def decodeName(url):
    return unicode(urllib.unquote(url), "utf-8") #.encode("utf-8")


def stripAccentMark(s):
    newstring = unicode()
    c = 0

    while c < len(s):
        if ord(s[c]) == 769: # ´ mark
            c += 1
            continue
        newstring += s[c]
        c += 1
    return newstring


def savenames2file(names):
    """
    Save names to a file. Saves bandwidth and nerves.
    """
    pickle.dump(names, open(fname_rusnames, "wb"))


def loadNamesFromFile():
    """
    Load names from a file. Saves bandwidth and nerves.
    """
    persons = pickle.load(open(fname_rusnames, "rb"))
    return persons


def fetchNames():
    listofnames = list()
    persons = list()
    i = 0
    skipped = 0

    with open("listofrussian.txt") as f:
        listofnames = f.readlines()

    for name in listofnames:
        name = name.rstrip("\n")
        wikipage = u"http://en.wikipedia.org/wiki/%s" % name

        r = requests.get(wikipage)
        if r == None:
            skipped += 1
            continue

        if verbose:
            print wikipage

        # Clean english name too
        e = name.find("(") - 1
        if e <= 0:
            e = len(name)
        name = name[0 : e]
        name = decodeName(name).replace("_", " ")
        runame = parseRuLang(r.content)

        if runame == None:
            skipped += 1
            continue

        person = Person(name, runame, wikipage)
        persons.append(person)

        i += 1
        print "[%4d / %3d / %3d] %s" % (i, len(listofnames), skipped, person)
    print "\n",

    return persons


def nameCompare(persons):
    for person in persons:
        en = person.en_name.split(" ")
        ru = person.ru_name.split(" ")
        ru = [stripAccentMark(name) for name in ru]

        # Transliterate English name to Russian name
        translit_ru = [translit(name, "ru") for name in en]

        for ru_litname in translit_ru:
            for ru_name in ru:
                print "'%s' (%d), '%s' (%d)" % (ru_litname, len(ru_litname), ru_name, len(ru_name))

                diff = SequenceMatcher(None, ru_litname, ru_name).ratio()
                if ru_litname == ru_name:
                    print "%s == %s" % (ru_name, ru_litname)
                elif diff > 0.75:
                    print "%s != %s (%.2f%%)" % (ru_name, ru_litname, diff)
            print
        break


def firstNameCompare(persons):
    i = 1

    while i < len(persons):
        prevname = persons[i - 1].en_name.split(" ")[0]
        curname  = persons[i].en_name.split(" ")[0]

        #print "%s:" % (prevname),
        print "%s:" % (persons[i - 1].en_name.split(" ")),

        while prevname == curname and i < len(persons):
            print "%s" % (", ".join(persons[i - 1].ru_name.split(" "))),
            i += 1
            curname = persons[i].en_name.split(" ")[0]
        print

        i += 1


def main():
    persons = list()

    if os.path.isfile(fname_rusnames):
        persons = loadNamesFromFile()
    else:
        print " %4s / %3s / %3s  %s" % ("Cur", "Ttl", "Err", "Person")
        print "#" * 25
        persons = fetchNames()
        savenames2file(persons)

    nameCompare(persons)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\nCTRL-C pressed"

