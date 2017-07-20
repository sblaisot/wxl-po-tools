#!/usr/bin/env python
# coding:utf-8

"""wxl2pot.py: Transform wxl localization files to pot format."""

__author__ = "Sébastien Blaisot (sebastien@blaisot.org)"
__copyright__ = "Copyright (C) 2016-2017 Sébastien Blaisot"
__license__ = "GPL 3.0"
__version__ = "0.1"
__status__ = "Development"

import getopt
import sys
import textwrap
import os.path
from xml.dom import minidom

import polib

def version():
    print os.path.basename(__file__) + " version " + __version__ + "\n"

def help():
    print textwrap.dedent("""\
      Usage: %s [OPTION]... WXL_SOURCE_FILE POT_DEST_FILE
      Transform the file WXL_SOURCE_FILE in wxl format into a pot file POT_DEST_FILE
      Example: %s -l LangId en-us.wxl en-us.pot

      Options:
        -h, --help:            print this help message and exit
        -V, --version          print version information and exit
        -f, --force            don't ask before overwriting destination file
        -l, --langid=LANGID    ignore string with Id LANGID containing the LCID
""" % (os.path.basename(__file__), os.path.basename(__file__)))

def usage():
    print textwrap.dedent("""\
      Usage: %s [OPTION]... WXL_SOURCE_FILE POT_DEST_FILE
      Try '%s --help' for more information.
    """ % (os.path.basename(__file__), os.path.basename(__file__)))


# Main

langid = ""
force = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "hVfl:", ["help", "version", "force", "langid="])
except getopt.GetoptError as err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
output = None
verbose = False
for o, a in opts:
    if o in ("-V", "--version"):
        version()
        sys.exit()
    elif o in ("-h", "--help"):
        help()
        sys.exit()
    elif o in ("-f", "--force"):
        force = True
    elif o in ("-l", "--langid"):
        langid = a
    else:
        assert False, "unhandled option"

if len(args) < 2:
    print "Missing filename parameters"
    usage()
    sys.exit(1)

sourcefile = args[0]
destfile = args[1]

if not os.path.exists(sourcefile):
    print "Source file " + sourcefile + " does not exist. Please provide a valid wxl file."
    sys.exit(1)

if os.path.exists(destfile) and not force:
    sys.stdout.write("Destination file " + destfile + " already exists. Overwrite ? [y/N] ")
    choice = raw_input().lower()
    if choice not in ['yes','y', 'ye']:
        print "Aborting"
        sys.exit(1)

doc = minidom.parse(sourcefile)

wixloc = doc.getElementsByTagName("WixLocalization")[0]
culture = wixloc.getAttribute("Culture")
codepage = wixloc.getAttribute("Codepage")

po = polib.POFile(wrapwidth=0)
po.metadata = {
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
}

root = doc.documentElement
nodes = root.childNodes

comment = ""

for node in nodes:
    if node.nodeType == node.COMMENT_NODE:
        if not comment:
            comment = node.data
        else:
            comment = comment+ "\n" + node.data
    if node.nodeType == node.ELEMENT_NODE:
        if node.tagName == "String":
            stringId = node.getAttribute("Id")
            if stringId == langid:
                comment = ""
                continue

            stringContent = node.firstChild.data
            entry = polib.POEntry(
                comment = comment,
                msgctxt = stringId,
                msgid = stringContent
            )
            po.append(entry)
            if comment != "":
                comment = ""
po.save(destfile)
