#!/usr/bin/env python
# encoding: utf-8
"""
delicious_import.py

Created by Hilary Mason on 2010-11-28.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import urllib
from xml.dom import minidom
from optparse import OptionParser

from gitmark import gitMark

class delicious_import(object):
    def __init__(self, username, password=''):
		# API URL: https://user:passwd@api.del.icio.us/v1/posts/all
        url = "https://%s:%s@api.del.icio.us/v1/posts/all" % (username, password)
        h = urllib.urlopen(url)
        content = h.read()
        h.close()
                
        x = minidom.parseString(content)
        
        # sample post: <post href="http://www.pixelbeat.org/cmdline.html" hash="e3ac1d1e4403d077ee7e65f62a55c406" description="Linux Commands - A practical reference" tag="linux tutorial reference" time="2010-11-29T01:07:35Z" extended="" meta="c79362665abb0303d577b6b9aa341599" />
        for post in x.getElementsByTagName("post"):
            url = post.getAttribute('href')
            desc = post.getAttribute('description')
            tags = ",".join([t for t in post.getAttribute('tag').split()])
            timestamp = post.getAttribute('time')
            
            options = {}
            options['tags'] = tags
            options['push'] = False
            options['msg'] = desc
            
            args = [url]

            g = gitMark(options, args)
        

if __name__ == '__main__':
    try:
        (username, password) = sys.argv[1:]
    except ValueError:
        print "Usage: python delicious_import.py username password"
        
    d = delicious_import(username, password)

