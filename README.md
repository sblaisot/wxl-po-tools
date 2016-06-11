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

These tools are written in python and use `xml.dom.minidom` and `polib`

`xml.dom.minidom` comes from the standard python distribution.

`polib` can be installed with `pip install polib`

wxl2pot.py
----------

Usage: `wxl2pot.py [OPTION]... WXL_SOURCE_FILE POT_DEST_FILE`

Transform the file WXL_SOURCE_FILE in wxl format into a pot file POT_DEST_FILE

Example: `wxl2pot.py -l LangId en-us.wxl en-us.pot`

Options:
* `-h, --help`             print this help message and exit
* `-V, --version`          print version information and exit
* `-f, --force`            don't ask before overwriting destination file
* `-l, --langid=LANGID`    ignore string with Id LANGID containing the LCID

transwxl2po.py
--------------

Usage: `transwxl2pot.py [OPTION]... WXL_SOURCE_FILE WXL_TRANSLATED_FILE POT_DEST_FILE`

Transform the file WXL_SOURCE_FILE in wxl format into a po file POT_DEST_FILE
containing the translations from WXL_TRANSLATED_FILE

Example: `transwxl2pot.py -l LangId en-us.wxl fr-fr.wxl fr-fr.po`

Options:
* `-h, --help`             print this help message and exit
* `-V, --version`          print version information and exit
* `-f, --force`            don't ask before overwriting destination file
* `-l, --langid=LANGID`    ignore string with Id LANGID containing the LCID

po2wxl.py
---------

Usage: `po2wxl.py [OPTION]... PO_SOURCE_FILE WXL_DEST_FILE`

Transform the file PO_SOURCE_FILE in po format into a wxl file WXL_DEST_FILE

Example: `po2wxl.py -l LangId en-us.po en-us.wxl`

Options:
* `-h, --help`                print this help message and exit
* `-V, --version`             print version information and exit
* `-f, --force`            don't ask before overwriting destination file
* `-l, --langid=LANGID`       automatically determine LCID based on language and add a string with id LANGID containing the LCID
* `-L, --LCID=LCID`           used with -l, use provided LCID instead of trying to guess it
* `-C, --codepage=CP`         use CP as codepage instead of trying to guess it
* `-p, --percentlimit=LIMIT`  do not translate po files which translation percent is below LIMIT. 60% by default

Licence
-------

These tools are licenced under the Gnu General Public Licence Version 3
