#!/usr/bin/python

import sys;
import os;
from xml.dom import minidom;
import polib;


if len(sys.argv) <= 3:
    print "Usage: transwxl2po.py <wxl file> <wxl translation> <pot file>";
    os._exit(1);

sourcefile = sys.argv[1];
transfile = sys.argv[2];
destfile = sys.argv[3];


transdoc = minidom.parse(transfile);

transwixloc = transdoc.getElementsByTagName("WixLocalization")[0];
transculture = transwixloc.getAttribute("Culture");

transculture = transculture[:transculture.index('-')] + '_' + transculture[(transculture.index('-') + 1):].upper();

transroot = transdoc.documentElement;
transnodes = transroot.childNodes;

translatedStrings = {};

for node in transnodes:
    if node.nodeType == node.ELEMENT_NODE:
        if node.tagName == "String":
            stringId = node.getAttribute("Id");
            stringContent = node.firstChild.data;
            translatedStrings[stringId] = stringContent;


doc = minidom.parse(sourcefile);

wixloc = doc.getElementsByTagName("WixLocalization")[0];
culture = wixloc.getAttribute("Culture");
codepage = wixloc.getAttribute("Codepage");

po = polib.POFile(wrapwidth=0);
po.metadata = {
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
    'Language': transculture
}

root = doc.documentElement;
nodes = root.childNodes;

comment = "";

for node in nodes:
    if node.nodeType == node.COMMENT_NODE:
        comment = node.data;
    if node.nodeType == node.ELEMENT_NODE:
        if node.tagName == "String":
            stringId = node.getAttribute("Id");
            stringContent = node.firstChild.data;
            if stringId in translatedStrings:
                translation = translatedStrings[stringId];
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
                comment = "";
po.save(destfile);
