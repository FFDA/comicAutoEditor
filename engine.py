#! /usr/bin/python3

### This file contains all functions that do actual work for comicAUtoEditor

from rarfile import RarFile # for cbr
from zipfile import ZipFile, ZIP_STORED # for cbz
from os import walk, sep, mkdir
from os.path import split, join, basename, expanduser
from tempfile import TemporaryDirectory
from re import compile, IGNORECASE

class Engine:

    def __init__(self):
        ## Creates ~/Comics directory if it doesn't exits.
        self.comic_save_location = expanduser("~") + "/Comics/" # Creating a path for the folder to create.
        try:
            mkdir(self.comic_save_location)
        except FileExistsError:
            # Folder already exists.
            pass

    def check_comic(self, comic_file, comic_file_name, comic_file_exte):
        ### Opens comic and checks files. Tries to find the one that is added by comic piracy group.
        ### Also detects if there is a subfolder in archive. Some groups have a subfolder in their comic archive that has their name in it.

        sub_folder_toggle = 0
        thumbs_db = (0, "")

        filename_length_dict = dict() # Dictionary that will be used to add all different files sorted by the length. Idea is that all comic pages names will be the same length.

        ## Because zip and rar uses different modules it has to be detected and seperated.
        if comic_file_exte.lower() == ".cbz":
            comic = ZipFile(comic_file)
        else: 
            comic = RarFile(comic_file)
        
        for item in comic.namelist():
            # Splits every filename in the archive. If any of them has a "dirname" it toggles a switch and breaks.
            item = split(item)
            if item[0] != "":
                sub_folder_toggle = 1
                break
        
        ## Loops though all the files in the comic archive. Key is length of the filename, value - list that contains first filename that has the that length and count how many time that length of file name has been detected.
        for page in comic.namelist():
            if page.lower() == "thumbs.db":
                thumbs_db = (1, page)
            elif page[-3:].lower() == "jpg":
                if len(page) not in filename_length_dict:
                    # If filename length is not in dictionary adds that length as a key and filename and starts count at 1 as value (list)
                    filename_length_dict[len(page)] = [page, 1]
                else:
                    # If there is filename with that length in dictionary it adds to the count +1.
                    filename_length_dict[len(page)][1] += 1

        sorted_filename_length_dict = sorted(filename_length_dict.items()) # Sortes dictionary entries (comic pages) by the length of the filename.

        comic.close()

        return sorted_filename_length_dict, sub_folder_toggle, thumbs_db

    def write_comic(self, comic_file, comic_file_name, comic_file_exte, delete_files, remove_from_filename):
        ### Fixind comic file by copying all files to cbz archive skipping the file user wants to delete.

        cbz_comic_archive = ZipFile(self.comic_save_location + comic_file_name + "cbz", mode="w", compression=ZIP_STORED, allowZip64=True)
        # cbz_comic_archive = ZipFile(self.comic_save_location + comic_file_name + "cbz", mode="w", compression=ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True) # Commented out, because on python3.6 compresslevel and strict_timestamps are not supported

        ## Because zip and rar uses different modules it has to be detected and seperated.
        if comic_file_exte.lower() == ".cbz":
            comic = ZipFile(comic_file, mode="r")
        else: 
            comic = RarFile(comic_file, mode="r")

        ## Extracting files from original comic archive and compresing them to new one without the file that user wants to delete. It opens a temp dir that is deleted after use.
        with TemporaryDirectory() as dir:
            
            for page in comic.namelist():
            ## Goes through every page of orginal archive again. Looks for a filename that matches the one that user wants to delete. Skips it and prints a message that it is deleted. The rest files are saved in temp directory
                if page not in delete_files:
                    comic.extract(page, dir) # Extracts file to full path, so if archive has a subfolder it will be created too.

            for folder in walk(dir):
            ## Goes through directories and files in temp directory.
                for page in folder[2]:
                    # Walk function returns tuple with three values, first one (foler[0]) is path to folder and third one (folder[2] is file list.)
                    # This loop goes through every folder of temp dir and and uses full path to point to a file, but tells to use just filename when writing to archive.
                    # It also removes part of the filename if user provides a string for it.
                    if len(remove_from_filename) == 0:
                        cbz_comic_archive.write(join(folder[0], page), arcname=basename(page)) 
                    else:
                        # If list remove_from_filename has at least one element it will remove that part from the filename when writing it to archive if it can find it.
                        cbz_comic_archive.write(join(folder[0], page), arcname=basename(page.replace(remove_from_filename[0], remove_from_filename[1])))

        cbz_comic_archive.close() # Closes new comics archive.
        

    def archive_file_list(self, comic_file, comic_file_name, comic_file_exte):
        ### Gets all files in the archive and returns them

        archive_file_list = []

        ## Because zip and rar uses different modules it has to be detected and seperated.
        if comic_file_exte.lower() == ".cbz":
            comic = ZipFile(comic_file)
        else: 
            comic = RarFile(comic_file)
        
        for item in comic.namelist():
        ## Appends every filename in the archive to the archive_file_list list
            if item.endswith("/"):
                pass
            else:
                archive_file_list.append(item)

        return archive_file_list

    def convert_to_cbz(self, comic_file, comic_file_name):
        ### This function only converts comic's archive to cbz without deleting files or folders
        ### I do not know what will happen if there would be two folders inside archive. Maybe one day I'll find out.

        cbz_comic_archive = ZipFile(self.comic_save_location + comic_file_name + ".cbz", mode="w", compression=ZIP_STORED, allowZip64=True)
        # cbz_comic_archive = ZipFile(comic_save_location + comic_file_name + "cbz", mode="w", compression=ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True) # Commented out, because on python3.6 compresslevel and strict_timestamps are not supported

        with TemporaryDirectory() as dir:
            ## Opens temporary directory named dir, that will be deleted when everything inside with statement is finished
            
            comic = RarFile(comic_file, mode="r") # Opening rar comic archive in read mode
            comic.extractall(path=dir) # Extracting every file to temporary directory
            
            base = "" # To save folder if one exists.

            for folder in walk(dir):
            ## Looping thought all folders/files
                if folder[1] != []:
                    base = folder[1][0]
                else:
                    for page in folder[2]:
                        # Adding every file in temporary dir to the archive
                        cbz_comic_archive.write(join(folder[0], page), arcname=join(base + sep + page))
