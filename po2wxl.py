#!/usr/bin/python

# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import os;
import polib;


if len(sys.argv) <= 2:
    print "Usage: wxl2pot.py <wxl file> <pot file>";
    os._exit(1);

sourcefile = sys.argv[1];
destfile = sys.argv[2];

po = polib.pofile(sourcefile);

metadata = po.ordered_metadata();
language = [value for name, value in metadata if name == "Language"]

culture=language[0].lower().replace('_','-');

f = open(destfile,'w');
f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n");
f.write("<WixLocalization Culture=\"" + culture + "\" Codepage=\"1252\"\n");
f.write("                 xmlns=\"http://schemas.microsoft.com/wix/2006/localization\">\n");


for entry in po:
    if entry.comment != "":
        f.write("\n");
        f.write("  <!--" + entry.comment + " -->\n");
    if entry.msgstr != "":
        translation = entry.msgstr;
    else:
        translation = entry.msgid;
    translation = "&#13;&#10;".join(translation.split("\n")).replace('\r', '');
    f.write("  <String Id=\"" + entry.msgctxt + "\">" + translation + "</String>\n");

f.write("</WixLocalization>\n");
f.close;
