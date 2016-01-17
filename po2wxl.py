#!/usr/bin/env python
# coding:utf-8

"""po2wxl.py: Transform a .po translation file into a wxl localization file"""

__author__ = "Sébastien Blaisot (sebastien@blaisot.org)"
__copyright__ = "Copyright (C) 2016 Sébastien Blaisot"
__license__ = "GPL 3.0"
__version__ = "0.1"
__status__ = "Development"

import getopt
import sys  
import textwrap
import os.path

import polib

from lcid import LCIDs

def version():
    print os.path.basename(__file__) + " version " + __version__ + "\n"

def help():
    print textwrap.dedent("""
      Usage: %s [OPTION]... PO_SOURCE_FILE WXL_DEST_FILE
      Transform the file PO_SOURCE_FILE in po format into a wxl file WXL_DEST_FILE
      Example: %s -l LangId en-us.po en-us.wxl

      Options:
        -h, --help:               print this help message and exit
        -V, --version             print version information and exit
        -f, --force            don't ask before overwriting destination file
        -l, --langid=LANGID       automatically determine LCID based on language and 
                                  add a string with id LANGID containing the LCID
        -L, --LCID=LCID           used with -l, use provided LCID instead of trying
                                  to guess it
        -C, --codepage=CP         use CP as codepage instead of trying to guess it
        -p, --percentlimit=LIMIT  do not translate po files which translation percent
                                  is below LIMIT. 60% by default
""" % (os.path.basename(__file__), os.path.basename(__file__)))

def usage():
    print textwrap.dedent("""\
      Usage: %s [OPTION]... PO_SOURCE_FILE WXL_DEST_FILE
      Try '%s --help' for more information.
    """ % (os.path.basename(__file__), os.path.basename(__file__)))


# Main
langid = ""
codepage = ""
LCID=""
translationPercentLimit = 60
force = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "hVfl:L:C:p:", ["help", "version", "force", "langid=", "LCID=", "codepage=", "percentlimit="])
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
    elif o in ("-L", "--LCID"):
        LCID = a
    elif o in ("-C", "--codepage"):
        codepage = a
    elif o in ("-p", "--percentlimit"):
        translationPercentLimit = int(a)
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

po = polib.pofile(sourcefile)

if po.percent_translated() <= translationPercentLimit:
    print "Skipping " + sourcefile + ": translated at " + str(po.percent_translated()) + "%, below the " + str(translationPercentLimit) + "% limit\n"
    sys.exit(0)

metadata = po.ordered_metadata()
language = [value for name, value in metadata if name == "Language"]

culture = language[0].lower().replace('_','-')
cultureShort = culture[:2];

if codepage == "":
    if culture in LCIDs.keys():
        codepage = LCIDs[culture]['codepage']
    elif cultureShort in LCIDs.keys():
        codepage = LCIDs[cultureShort]['codepage']
    else:
        print "Unable to guess codepage based on language " + culture
        print "Please provide codepage with option -C"
        print "Try 'po2wxl.py --help' for more information."
        sys.exit(1)

if not codepage:
    codepage = "65001" # UTF-8 fallback

if LCID != "":
    langIdAuto = LCID
else:
    if culture in LCIDs.keys():
        langIdAuto = LCIDs[culture]['LCID']
    elif cultureShort in LCIDs.keys():
        langIdAuto = LCIDs[cultureShort]['LCID']
    else:
        print "Unable to guess LCID based on language " + culture
        print "Please provide LCID with option -L"
        print "Try 'po2wxl.py --help' for more information."
        sys.exit(1);
    

f = open(destfile,'w')
f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
f.write("<WixLocalization Culture=\"" + culture + "\" Codepage=\"" + str(codepage) + "\"\n")
f.write("                 xmlns=\"http://schemas.microsoft.com/wix/2006/localization\">\n")
f.write("\n")
f.write("  <!-- .................................................... -->\n")
f.write("  <!-- This wxl file has been auto generated from a po file -->\n")
f.write("  <!-- using https://github.com/sblaisot/wxl-po-tools       -->\n")
f.write("  <!-- Source File: " + sourcefile.ljust(39) + " -->\n")
f.write("  <!-- .................................................... -->\n")
f.write("\n")

if langid:
    f.write("  <!-- This contains the LangID and should be translated to reflect the correct LangID. -->\n")
    f.write("  <!-- Supported language and codepage codes can be found here: https://msdn.microsoft.com/en-us/goglobal/bb964664.aspx -->\n")
    f.write("  <String Id=\"" + langid + "\">" + str(langIdAuto) + "</String>\n")
    f.write("\n")

for entry in po:
    if entry.comment != "":
        f.write("\n")
        f.write("  <!--" + entry.comment.replace('\n', ' -->\n  <!--') + " -->\n")
    if entry.msgstr != "":
        translation = entry.msgstr
    else:
        translation = entry.msgid
    translation = "&#13;&#10;".join(translation.split("\n")).replace('\r', '')
    f.write("  <String Id=\"" + entry.msgctxt.encode("utf-8") + "\">" + translation.encode("utf-8") + "</String>\n")

f.write("</WixLocalization>\n")
f.close
