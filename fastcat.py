#!/usr/bin/env python

import os
import re
import bz2
import urllib

import redis

skos_file = "skos.nt.bz2"
db = redis.Redis()

def broader(cat):
    """Pass in a Wikipedia category and get back a list of broader Wikipedia
    categories.
    """
    return list(db.smembers("b:%s" % cat))

def narrower(cat):
    """Pass in a Wikipedia category and get back a list of narrower Wikipedia
    categories.
    """
    return list(db.smembers("n:%s" % cat))

def load_db():
    if not os.path.isfile(skos_file):
        download()

    p = re.compile('^<(.+)> <(.+)> <(.+)> \.$') 
    for line in bz2.BZ2File(skos_file):
        m = re.match(p, line.strip())
        
        if not m: continue
        s, p, o = m.groups()

        # only interested in broader relation
        if p != "http://www.w3.org/2004/02/skos/core#broader":
            continue

        add(name(s), name(o))

def add(narrower, broader):
    db.sadd("b:%s" % narrower, broader)
    db.sadd("n:%s" % broader, narrower)
    print ("added %s -> %s" % (broader, narrower)).encode('utf-8')

def download():
    print "downloading wikipedia skos file from dbpedia"
    url = "http://downloads.dbpedia.org/current/en/skos_categories_en.nt.bz2"
    urllib.urlretrieve(url, skos_file)

def name(cat_url):
    m = re.search("^http://dbpedia.org/resource/Category:(.+)$", cat_url)
    return urllib.unquote(m.group(1).replace("_", " ")).decode("utf-8")


# first time this module is loaded it'll try to download the skos file 
# and load it into Redis

if not db.get("cat-loaded"):
    load_db()
    db.set("cat-loaded", "1")
