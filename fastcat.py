#!/usr/bin/env python

import os
import re
import bz2
import urllib

import redis

skos_file = "skos.nt.bz2"

class FastCat(object):

    def __init__(self, db=None):
        if db == None:
            db = redis.Redis()
        self.db = db

    def broader(self, cat):
        """Pass in a Wikipedia category and get back a list of broader Wikipedia
        categories.
        """
        return list(self.db.smembers("b:%s" % cat))

    def narrower(self, cat):
        """Pass in a Wikipedia category and get back a list of narrower Wikipedia
        categories.
        """
        return list(self.db.smembers("n:%s" % cat))

    def load(self):
        if not os.path.isfile(skos_file):
            self.download()

        ntriple_pattern = re.compile('^<(.+)> <(.+)> <(.+)> \.$') 
        for line in bz2.BZ2File(skos_file):
            line = line.strip()
            m = ntriple_pattern.match(line)
            
            if not m: 
                continue
            s, p, o = m.groups()

            # only interested in broader relation
            if p != "http://www.w3.org/2004/02/skos/core#broader":
                continue

            self._add(self.name(s), self.name(o))

    def _add(self, narrower, broader):
        self.db.sadd("b:%s" % narrower, broader)
        self.db.sadd("n:%s" % broader, narrower)
        print ("added %s -> %s" % (broader, narrower)).encode('utf-8')

    def download(self):
        print "downloading wikipedia skos file from dbpedia"
        url = "http://downloads.dbpedia.org/current/en/skos_categories_en.nt.bz2"
        urllib.urlretrieve(url, skos_file)

    def name(self, cat_url):
        m = re.search("^http://dbpedia.org/resource/Category:(.+)$", cat_url)
        return urllib.unquote(m.group(1).replace("_", " ")).decode("utf-8")
