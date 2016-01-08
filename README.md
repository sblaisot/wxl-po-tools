wxl-po-tools
============

Introduction
------------

This set of tools is intended to help using translation tools and platforms (like transifex for exemple) to translate your wxl translation files from wix.
Wix is a windows framework to build MSI installation files that can produce localized installers using XML files containing the localized strings (called wxl files). Unfortunately, a lot (if not most) of the translation platforms can't work with these files.

wxl-po-tools contains 3 small utilities that help "translate" your wxl files into standard GNU's gettext po files that can be used on any translation tool or platform and to convert back the translated po file to a wxl file.
You can also convert a wxl source file and a wxl translated file into a single translated po file.

Requirements
------------

These tools are written in python and use xml.dom.minidom and polib

xml.dom.minidom comes from the standard python distribution.

polib can be installed with `pip install polib`

wxl2pot.py
----------

Usage:
`wxl2pot.py <wxl_sourcefile> <pot_destfile>`

read the wxl_sourcefile content and produces a pot file (typically a po file without any translation) as pot_destfile

transwxl2po.py
--------------

Usage:
`transwxl2po.py <wxl_sourcefile> <wxl_translationfile> <translated_po_destfile>`

Read the original wxl file and a translated one and create a translated po file as translated_po_destfile

po2wxl.py
---------

Usage:
`po2wxl.py <po_sourcefile> <wxl_destfile>`

read the translation from po_sourcefile content and produces a wxl file as wxl_destfile

Licence
-------

These tools are licenced under the Gnu General Public Licence Version 3

