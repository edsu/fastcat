#!/usr/bin/env python

import os
import re
import bz2
import urllib

import redis

articles_file = "articles.nt.bz2"
skos_file = "skos.nt.bz2"
ntriple_pattern = re.compile('^<(.+)> <(.+)> <(.+)> \.\n$') 

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
        self.load_skos()
        # disabling this unless it can be more memory efficient
        #self.load_articles()

    def load_skos(self):
        if self.db.get("loaded-skos"):
            return 

        if not os.path.isfile(skos_file):
            self.download_skos()

        print "loading %s" % skos_file
        for line in bz2.BZ2File(skos_file):
            m = ntriple_pattern.match(line)
            
            if not m: 
                continue

            s, p, o = m.groups()
            if p != "http://www.w3.org/2004/02/skos/core#broader":
                continue

            narrower = self._category_name(s)
            broader = self._category_name(o)
            self.db.sadd("b:%s" % narrower, broader)
            self.db.sadd("n:%s" % broader, narrower)
            print ("added %s -> %s" % (broader, narrower)).encode('utf-8')

        self.db.set("loaded-skos", "1")

    def load_articles(self):
        if self.db.get("loaded-articles"):
            return

        if not os.path.isfile(articles_file):
            self.download_articles()

        print "loading %s" % articles_file
        for line in bz2.BZ2File(articles_file):
            m = ntriple_pattern.match(line)
            
            if not m: 
                print line
                continue
            s, p, o = m.groups()
            if p != "http://purl.org/dc/terms/subject":
                continue
            
            page = self._article_name(s)
            category = self._category_name(o)
            self.db.sadd("p:%s" % page, category)
            self.db.sadd("c:%s" % category, page)
            print ("added page %s (%s)" % (page, category)).encode('utf-8')

        self.db.set("loaded-articles", "1")

    def download_skos(self):
        print "downloading wikipedia skos file from dbpedia"
        url = "http://downloads.dbpedia.org/current/en/skos_categories_en.nt.bz2"
        urllib.urlretrieve(url, skos_file)

    def download_articles(self):
        print "downloading article categories file from dbpedia"
        url = "http://downloads.dbpedia.org/current/en/article_categories_en.nt.bz2"
        urllib.urlretrieve(url, skos_file)

    def _article_name(self, url):
        m = re.search("^http://dbpedia.org/resource/(.+)$", url)
        return urllib.unquote(m.group(1).replace("_", " ")).decode("utf-8")

    def _category_name(self, url):
        m = re.search("^http://dbpedia.org/resource/Category:(.+)$", url)
        return urllib.unquote(m.group(1).replace("_", " ")).decode("utf-8")
