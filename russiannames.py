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
from nltk.util import ngrams

from Person import Person

verbose = 0
total = 0
totalcorrect = 0
fname_rusnames = "rusnames.dump"
fliterated_name = "literated.txt"


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


def jaccardIdx(w1, w2):
    w1ngrams = set(ngrams(w1, 2))
    w2ngrams = set(ngrams(w2, 2))

    union = w1ngrams.union(w2ngrams)
    intersect = w1ngrams.intersection(w2ngrams)

    return 1.0 - float(len(intersect)) / float(len(union))


def nameCompare(persons, percentage = float(0.50)):
    global total, totalcorrect

    for person in persons:
        en = person.en_name.split(" ")
        ru = person.ru_name.split(" ")
        ru = [stripAccentMark(name) for name in ru]

        # Transliterate english name to russian name
        translit_ru = [translit(name, "ru") for name in en]
        translit_en = [translit(name.encode("utf-8").decode("utf-8"), \
                reversed = True) for name in ru]

        total += len(en)

        # Print name in english and russian
        yield u"\n%s (EN) %s (RU) " % (" ".join(en), " ".join(ru))

        for en_litname in translit_en:
            for en_name in en:
                diff = jaccardIdx(en_name, en_litname)
                if diff <= percentage:
                    if diff == 0.0:
                        totalcorrect += 1
                    yield u":: (EN orig) %s <==> (EN lit) %s (%.2f)" % (en_name, \
                           en_litname, diff)


def firstNameCompare(persons):
    i = 1

    while i < len(persons):
        prevname = persons[i - 1].en_name.split(" ")[0]
        curname  = persons[i].en_name.split(" ")[0]

        print "%s:" % (persons[i - 1].en_name.split(" ")),

        while prevname == curname and i < len(persons):
            print "%s" % (", ".join(persons[i - 1].ru_name.split(" "))),
            i += 1
            curname = persons[i].en_name.split(" ")[0]
        print

        i += 1


def main():
    global total, totalcorrect
    persons = list()
    fliterated = None

    if os.path.isfile(fname_rusnames):
        persons = loadNamesFromFile()
    else:
        print " %4s / %3s / %3s  %s" % ("Cur", "Ttl", "Err", "Person")
        print "#" * 25
        persons = fetchNames()
        savenames2file(persons)

    try:
        fliterated = open(fliterated_name, "wb")
    except IOError, ie:
        print "Cannot open file literated.txt for saving"
        sys.exit(1)

    for name in nameCompare(persons, 0.70):
        fliterated.write("%s\n" % name.encode("utf-8"))

    # Print statistics
    fliterated.write("\n-----------------\n")
    fliterated.write("Total %d entries" % len(persons))
    fliterated.write("\nWhere equal transliterations %d of total %d" % \
            (totalcorrect, total))

    fliterated.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\nCTRL-C pressed"

