# comicAutoEditor

This script removes unwanted images from comics archives (cbr, cbz) by creating new one from content of provided comic archive. During this proccess it removes subfolders if there are any in the archive.

All comic archives created with this script will be cbz (zip based), because of rar licensing.

# How to

Just run script in the folder with cbr or cbz file and follow the prompts (One).

One argument can be passed to a script: -s. It removes # from filename of the file if it has any, because Calibre do not accept file with # in them.

# Requirements

* Python3
* rarfile package for Python3