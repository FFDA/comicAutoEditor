# comicAutoEditor

![comicAutoEditor window](https://i.imgur.com/N9Cqsfj.png)

This script removes unwanted images from comics archives (cbr, cbz) by creating a new one from content of provided comic archive. During this proccess it removes subfolders and thumbs.db (and other) files if there are any in the archive.

All comic archives created with this script will be cbz (zip based), because of rar licensing.

It can also remove or replace parts of the filenames inside of the archive.

Version 1.0+ has a GUI made with PyQt5


# How to

Just run script (comicAutoEditor.py) in the folder with cbr or cbz file and follow the prompts. If you use a GUI version you don't have to launch program in folder with comics in them. Just launch it and using "Select Comic" choose a comics file to edit.

One argument can be passed to a script: -s. It removes # from filename of the file if it has any, because (some versions of) Calibre do not accept files with # in them.

To lauch GUI version run comicAutoEditor-gui.py with python. Don't forget to install PyQt5.


# Requirements

* Python3
* rarfile package for Python3
* PyQt5
