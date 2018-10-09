#! /usr/bin/python3
# -*- coding: utf8 -*-

import cgitb; cgitb.enable()
import os

print ("Content-Type: text/plain\r\n")

for k, v in os.environ.items():
    print ("%s: %s" % (k, v))
