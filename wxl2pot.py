#!/usr/bin/python

import sys;
import os;
from xml.dom import minidom;
import polib;


if len(sys.argv) <= 2:
	print "Usage: wxl2pot.py <wxl file> <pot file>";
	os._exit(1);

sourcefile = sys.argv[1];
destfile = sys.argv[2];

doc = minidom.parse(sourcefile);

wixloc = doc.getElementsByTagName("WixLocalization")[0];
culture = wixloc.getAttribute("Culture");
codepage = wixloc.getAttribute("Codepage");

po = polib.POFile(wrapwidth=0);
po.metadata = {
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
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
			entry = polib.POEntry(
				comment = comment,
				msgctxt = stringId,
				msgid = stringContent
			)
			po.append(entry)
			if comment != "":
				comment = "";
po.save(destfile);
