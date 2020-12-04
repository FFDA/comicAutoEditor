#! /usr/bin/python

#### This program extrackts all cbz and cbr files in the directory one by one, finds files added by release grupe, asks user to choose file to delete or confirm default removes them and compresses them back to cbz. 
#### Compresses file to cbz, because there is no free implementation of rar compresion because of licensing by the creator.
#### New file will saved in home directory "comics" folder (~/comics) to skip avoid problems with same filename in one folder. Also user might not want to delete the original archive by runnign this program.
 
from rarfile import RarFile # for cbr
from zipfile import ZipFile, ZIP_STORED # for cbz
from os import listdir, mkdir
from os.path import expanduser, abspath, join
from sys import exit
from tempfile import TemporaryDirectory

def check_comic(file, file_name, file_exte):
    ### Opens comic and checks files. Tries to find the one that is added by comic piracy group.

    filename_length_dict = dict() # Dictionary that will be used to add all different files sorted by the length. Idea is that all comic pages names will be the same length.

    ## Because zip and rar uses different modules it has to be detected and seperated.
    if file_exte.lower() == "cbz":
        comic = ZipFile(file)
    else: 
        comic = RarFile(file)
    
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
    
    ## Promts user to choose what file to delete, by printing sorted dictionary.
    print("Delete item:")
    for item in range(len(sorted_filename_length_dict)):
        print(str(item) + ". " + str(sorted_filename_length_dict[item][1][0]))
    print("x. Skip")

    user_choice = input("[<ENTER> default = 0] ") # Saved user choise

    ## Sorting user choice.
    if user_choice.lower() == "x":
        print("Skipping")
        pass
    elif user_choice == "":
        # Detecting <ENTER>
        delete_file = sorted_filename_length_dict[0][1][0]
        print("Deleting: " + delete_file)
        write_comic(file, file_name, file_exte, delete_file)
    elif int(user_choice) in range(len(sorted_filename_length_dict)):
        delete_file = sorted_filename_length_dict[int(user_choice)][1][0]
        print("Deleting: " + delete_file)
    else:
        # Not valid user input
        print("There is no such option. Skipping to next step.")

    comic.close()

def write_comic(file, file_name, file_exte, delete_file):
    ### Fixind comic file by copying all files to cbz archive skipping the file user wants to delete.

    print("Opening cbz") # Test line. Will be deleted.
    cbz_comic_archive = ZipFile(comic_save_location + file_name + "cbz", mode="w", compression=ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True)

    ## Because zip and rar uses different modules it has to be detected and seperated.
    if file_exte.lower() == "cbz":
        comic = ZipFile(file)
    else: 
        comic = RarFile(file)

    ## Extracting files from original comic archive and compresing them to new one without the file that user wants to delete. It opens a temp dir that is deleted after use.
    with TemporaryDirectory() as dir:

        temp_dir_path = abspath(dir) # Needed to point to file location
        
        for page in comic.namelist():
        ## Goes throught every page of orginal archive again. Looks for a filename that matches the one that user wants to delete. Skips it and prints a message that it is deleted. The rest files are saved in temp directory
            if page != delete_file:
                comic.extract(page, dir)
            else:
                print("Deleted " + delete_file)

        for f in listdir(dir):
        ## Goes through files in temp directory
            cbz_comic_archive.write(join(temp_dir_path, f))

    cbz_comic_archive.close() # Closes new comics archive.

current_dir_files = listdir() # Getting all the filenames in current working dir

## Creates ~/Comics directory if it doesn't exits.
comic_save_location = expanduser("~") + "/Comics/" # Creating a path for the folder to create.
try:
    mkdir(comic_save_location)
except FileExistsError:
    # Folder already exists.
    pass


for file in current_dir_files:
    ## Loops thought all the files and passes the allong if they have "cbz" or "cbr" extention.
    if file[-3:] == "cbz" or file[-3:] == "cbr":
        file_name = file[:-3] # Variable saves file name
        file_exte = file[-3:] # Variable saves file extention
        print(file_name)
        print()
        print("*********************")
        print("Working on: " + file)
        check_comic(file, file_name, file_exte) # Sends file for processing

exit()