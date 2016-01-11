#!/usr/bin/python

# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import getopt, textwrap
import polib
from lcid import LCIDs

def version():
    print "po2wxl.py version 0.1\n"

def help():
    print textwrap.dedent("""
      Usage: po2wxl.py [OPTION]... PO_SOURCE_FILE WXL_DEST_FILE
      Transform the file PO_SOURCE_FILE in po format into a wxl file WXL_DEST_FILE
      Example: po2wxl.py -l LangId en-us.po en-us.wxl

      Options:
        -h, --help:               print this help message and exit
        -V, --version             print version information and exit
        -l, --langid=LANGID       automatically determine LCID based on language and 
                                  add a string with id LANGID containing the LCID
        -p, --percentlimit=LIMIT  do not translate po files which translation percent
                                  is below LIMIT. 60% by default
""")

def usage():
    print textwrap.dedent("""\
      Usage: po2wxl.py [OPTION]... PO_SOURCE_FILE WXL_DEST_FILE
      Try 'po2wxl.py --help' for more information.
    """)


# Main
langid = ""
translationPercentLimit = 60
try:
    opts, args = getopt.getopt(sys.argv[1:], "hVl:p:", ["help", "version", "langid=", "percentlimit="])
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
    elif o in ("-l", "--langid"):
        langid = a
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

po = polib.pofile(sourcefile)

if po.percent_translated() <= translationPercentLimit:
    print "Skipping " + sourcefile + ": translated at " + str(po.percent_translated()) + "%, below the " + str(translationPercentLimit) + "% limit\n"
    sys.exit(0)

metadata = po.ordered_metadata()
language = [value for name, value in metadata if name == "Language"]

culture = language[0].lower().replace('_','-')
cultureShort = culture[:2];

if culture in LCIDs.keys():
    langIdAuto = LCIDs[culture]['LCID']
    codepage = LCIDs[culture]['codepage']
elif cultureShort in LCIDs.keys():
    langIdAuto = LCIDs[cultureShort]['LCID']
    codepage = LCIDs[cultureShort]['codepage']
else:
    print "Unknow language: " + culture + ", exiting\n";
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
    f.write("  <String Id=\"" + entry.msgctxt + "\">" + translation + "</String>\n")

f.write("</WixLocalization>\n")
f.close
