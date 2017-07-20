#!/usr/bin/env python
# coding:utf-8

"""transwxl2po.py: Transform a main language wxl file and a translated wxl file into a .po translation file"""

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
    print textwrap.dedent("""
      Usage: %s [OPTION]... WXL_SOURCE_FILE WXL_TRANSLATED_FILE PO_DEST_FILE
      Transform the file WXL_SOURCE_FILE in wxl format into a po file PO_DEST_FILE
      containing the translations from WXL_TRANSLATED_FILE
      Example: %s -l LangId en-us.wxl fr-fr.wxl fr-fr.po

      Options:
        -h, --help:            print this help message and exit
        -V, --version          print version information and exit
        -f, --force            don't ask before overwriting destination file
        -l, --langid=LANGID    ignore string with Id LANGID containing the LCID
""" % (os.path.basename(__file__), os.path.basename(__file__)))

def usage():
    print textwrap.dedent("""\
      Usage: %s [OPTION]... WXL_SOURCE_FILE WXL_TRANSLATED_FILE PO_DEST_FILE
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

if len(args) < 3:
    print "Missing filename parameters"
    usage()
    sys.exit(1)

sourcefile = args[0]
transfile = args[1]
destfile = args[2]

if not os.path.exists(sourcefile):
    print "Source file " + sourcefile + " does not exist. Please provide a valid wxl file."
    sys.exit(1)

if not os.path.exists(transfile):
    print "Translated file " + transfile + " does not exist. Please provide a valid wxl file."
    sys.exit(1)

if os.path.exists(destfile) and not force:
    sys.stdout.write("Destination file " + destfile + " already exists. Overwrite ? [y/N] ")
    choice = raw_input().lower()
    if choice not in ['yes','y', 'ye']:
        print "Aborting"
        sys.exit(1)

transdoc = minidom.parse(transfile)

transwixloc = transdoc.getElementsByTagName("WixLocalization")[0]
transculture = transwixloc.getAttribute("Culture")

transculture = transculture[:transculture.index('-')] + '_' + transculture[(transculture.index('-') + 1):].upper()

transroot = transdoc.documentElement
transnodes = transroot.childNodes

translatedStrings = {}

for node in transnodes:
    if node.nodeType == node.ELEMENT_NODE:
        if node.tagName == "String":
            stringId = node.getAttribute("Id")
            if stringId == langid:
                comment = ""
                continue
            stringContent = node.firstChild.data
            translatedStrings[stringId] = stringContent


doc = minidom.parse(sourcefile)

wixloc = doc.getElementsByTagName("WixLocalization")[0]
culture = wixloc.getAttribute("Culture")
codepage = wixloc.getAttribute("Codepage")

po = polib.POFile(wrapwidth=0)
po.metadata = {
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
    'Language': transculture
}

root = doc.documentElement
nodes = root.childNodes

comment = ""

for node in nodes:
    if node.nodeType == node.COMMENT_NODE:
        comment = node.data
    if node.nodeType == node.ELEMENT_NODE:
        if node.tagName == "String":
            stringId = node.getAttribute("Id")
            if stringId == langid:
                continue

            stringContent = node.firstChild.data
            if stringId in translatedStrings:
                translation = translatedStrings[stringId]
            else:
                translation = stringContent;
            entry = polib.POEntry(
                comment = comment,
                msgctxt = stringId,
                msgid = stringContent,
                msgstr = translation
            )
            po.append(entry)
            if comment != "":
                comment = ""
po.save(destfile)
