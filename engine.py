#! /usr/bin/python

### This file contains all functions that do actual work for comicAUtoEditor

from rarfile import RarFile # for cbr
from zipfile import ZipFile, ZIP_STORED # for cbz
from os import walk, sep
from os.path import split, join, basename
from tempfile import TemporaryDirectory

class Engine:

    def __init__(self):
        pass

    def check_comic(self, file, file_name, file_exte):
        ### Opens comic and checks files. Tries to find the one that is added by comic piracy group.
        ### Also detects if there is a subfolder in archive. Some groups have a subfolder in their comic archive that has their name in it.

        sub_folder_toggle = 0

        filename_length_dict = dict() # Dictionary that will be used to add all different files sorted by the length. Idea is that all comic pages names will be the same length.

        ## Because zip and rar uses different modules it has to be detected and seperated.
        if file_exte.lower() == "cbz":
            comic = ZipFile(file)
        else: 
            comic = RarFile(file)
        
        for item in comic.namelist():
            # Splits every filename in the archive. If any of them has a "dirname" it toggles a switch and breaks.
            item = split(item)
            if item[0] != "":
                print("")
                print("!!!Detected a sub folder in archive file!!!")
                print("It will be removed if any images will be removed.")
                print("Comic will still work normaly.")
                print("")
                sub_folder_toggle = 1
                break
        
        ## Loops though all the files in the comic archive. Key is length of the filename, value - list that contains first filename that has the that length and count how many time that length of file name has been detected.
        for page in comic.namelist():
            if page[-3:].lower() == "jpg":
                if len(page) not in filename_length_dict:
                    # If filename length is not in dictionary adds that length as a key and filename and starts count at 1 as value (list)
                    filename_length_dict[len(page)] = [page, 1]
                else:
                    # If there is filename with that length in dictionary it adds to the count +1.
                    filename_length_dict[len(page)][1] += 1

        sorted_filename_length_dict = sorted(filename_length_dict.items()) # Sortes dictionary entries (comic pages) by the length of the filename.

        comic.close()

        return sorted_filename_length_dict, sub_folder_toggle

    def write_comic(self, file, file_name, file_exte, delete_file, comic_save_location):
        ### Fixind comic file by copying all files to cbz archive skipping the file user wants to delete.

        cbz_comic_archive = ZipFile(comic_save_location + file_name + "cbz", mode="w", compression=ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True)

        ## Because zip and rar uses different modules it has to be detected and seperated.
        if file_exte.lower() == "cbz":
            comic = ZipFile(file)
        else: 
            comic = RarFile(file)

        ## Extracting files from original comic archive and compresing them to new one without the file that user wants to delete. It opens a temp dir that is deleted after use.
        with TemporaryDirectory() as dir:
            
            for page in comic.namelist():
            ## Goes through every page of orginal archive again. Looks for a filename that matches the one that user wants to delete. Skips it and prints a message that it is deleted. The rest files are saved in temp directory
                if page != delete_file:
                    comic.extract(page, dir) # Extracts file to full path, so if archive has a subfolder it will be created too.
                else:
                    # print("Deleted " + delete_file) # I might delete this message later
                    pass

            for folder in walk(dir):
            ## Goes through directories and files in temp directory.
                for page in folder[2]:
                    # Walk function returns tuple with tree values, first one (foler[0]) is path to filder and third one (folder[2] is file list.)
                    # This loop goes through every folder of temp dir and and uses full path to point to a file, but tells to use just filename when writing to archive.
                    cbz_comic_archive.write(join(folder[0] + sep + page), arcname=basename(page)) 

        cbz_comic_archive.close() # Closes new comics archive.
        print("Saved file: " + comic_save_location + file_name + "cbz")