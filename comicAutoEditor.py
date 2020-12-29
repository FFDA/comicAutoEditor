#! /usr/bin/python

#### This program extrackts all cbz and cbr files in the directory one by one, finds files added by release grupe, asks user to choose file to delete or confirm default removes them and compresses them back to cbz. 
#### Compresses file to cbz, because there is no free implementation of rar compresion because of licensing by the creator.
#### New file will saved in home directory "comics" folder (~/comics) to skip avoid problems with same filename in one folder. Also user might not want to delete the original archive by runnign this program.
#### Takes one argument -s (sanitize). Calibre to not take filenames with # in them. If user passes this argument filenames will be sanitized and # removed.
 
from os import listdir, mkdir
from os.path import expanduser
from sys import exit, argv
from engine import Engine

engine = Engine()

def user_promt_for_deletion():
    ## Promts user to choose what file to delete, by printing sorted dictionary containing some filenames that might be good for deleting and options for user to choose.
    print("............")
    print("Working on: " + file)
    print("")
    print("Delete item:")
    for item in range(len(sorted_filename_length_dict)):
        print(str(item) + ". " + str(sorted_filename_length_dict[item][1][0]))
    # print("............")
    print("")
    if sub_folder_toggle == 1 or thumbs_db[0] == 1:
        print("v. Only Detele Subfolder and/or thumbs.db")
    print("a. Print all files in comic archive and choose what to delete")
    if file_exte == "cbr":
        print("q. Only convert archive to cbz")
    print("d. Delete part of the filename from pages")
    print("x. Skip")
    print("............")
    print("")

    user_choice_parser(input("[<ENTER> default = 0] ")) # Sending user choice to user_choice_parser function.

def user_choice_parser(user_choice):
    ## Sorting user choice that was passed from user_promt_for_deletion.
    try:
        if user_choice.lower() == "x":
            print("Skipping")
            pass
        elif user_choice.lower() == "d":
            # User chose to remove part of the page filename. This elif statement asks user to write what needs to be deleted and appends it to remove_from_filename list.
            print("Type/copy part of the string you want to remove:")
            remove_from_filename.append(input())
            user_promt_for_deletion()
        elif user_choice.lower() == "a":
            # User chose to print all the files of the archive. Prints files, and askes user to choose any file for deletion.
            archive_file_list = engine.print_archive_files(file, file_name, file_exte) # Get's archives file list from engine.py function
            for item in range(len(archive_file_list)):
                print(str(item) + ". " + archive_file_list[item])
            print("")
            print("Do you want to delete any of these files?")
            extra_file_to_delete(archive_file_list)
        elif user_choice.lower() == "q":
            if file_exte == "cbr":
                engine.convert_to_cbz(file, file_name, comic_save_location)
            else:
                print("You shouldn't press random buttons. Skipping.")
        elif user_choice.lower() == "v":
            if sub_folder_toggle == 1 or thumbs_db[0] == 1:
                # Detecting user choice to delete subfolder only. Passing empty sting as file that needs to be deleted. That way nothing matching will be found and only folder will be removed.
                engine.write_comic(file, file_name, file_exte, delete_files, remove_from_filename, comic_save_location)
            else:
                print("There is no such option for this file. Skipping to next step.")
        elif user_choice == "":
            # Detecting <ENTER>
            chosen_file = sorted_filename_length_dict[0][1][0]
            if chosen_file not in delete_files:
                delete_files.append(chosen_file)
            else:
                print("This file already marked for deletion.")            
            # delete_files.append(sorted_filename_length_dict[0][1][0])
            # print("Deleting: " + ", ".join(delete_files))
            print("Deleting: ")
            print_file_list(delete_files)
            engine.write_comic(file, file_name, file_exte, delete_files, remove_from_filename, comic_save_location)
        elif int(user_choice) in range(len(sorted_filename_length_dict)):
            # User's choice where he/she chose to file themselves.
            chosen_file = sorted_filename_length_dict[int(user_choice)][1][0]
            if chosen_file not in delete_files:
                delete_files.append(chosen_file)
            else:
                print("This file already marked for deletion.")
            # print("Deleting: " + ", ".join(delete_files))
            print("Deleting:")
            print_file_list(delete_files)
            engine.write_comic(file, file_name, file_exte, delete_files, remove_from_filename, comic_save_location)
        else:
            # Not valid user input
            print("There is no such option. Skipping to next step.")
    except ValueError:
        print("There is no such option. Skipping to next step.")
        user_promt_for_deletion()

def extra_file_to_delete(archive_file_list):
    ## Function asking user to choose and extra file for deletion until <ENTER> is pressed.
    print("Type number of the file or <ENTER> to continue.")
    answer = input()
    while answer != "":
        if int(answer) in range(len(archive_file_list)):
        # If user typed number that is index of the file in archive_file_list
            if archive_file_list[int(answer)] not in delete_files:
            # If chosen filename is not in delete_files list
                delete_files.append(archive_file_list[int(answer)]) # Adding file to delete_files list
                print("Marked " + archive_file_list[int(answer)] + " for deletion.")
            else:
                print("File " + archive_file_list[int(answer)] + " is already marked for deletion.")
            print("")
            print("Another file?")
        else:
            print("There is no such file.")
        print("Type number of the file or <ENTER> to continue.")
        answer = input()
    
    # Prints all files that a currently marked for deletion
    if len(delete_files) > 0:
        print("Files marked for deletion:")
        print_file_list(delete_files)

    user_promt_for_deletion() # Printing previous menu.

def print_file_list(file_list):
    for page in file_list:
        print(page)
    print("")

current_dir_files = listdir() # Getting all the filenames in current working dir

## Creates ~/Comics directory if it doesn't exits.
comic_save_location = expanduser("~") + "/Comics/" # Creating a path for the folder to create.
try:
    mkdir(comic_save_location)
except FileExistsError:
    # Folder already exists.
    pass

for file in current_dir_files:

    delete_files = [] # List containing all filenames to delete
    thumbs_db = (0, "") # Tuple for detecting thumbs.db in archive
    remove_from_filename = [] # List for string that will be removed from page's filname if user provides it. Only first element will be used, other will be ignored.

    ## Loops thought all the files and passes the allong if they have "cbz" or "cbr" extention.
    if file[-3:] == "cbz" or file[-3:] == "cbr":

        file_name = file[:-3] # Variable saves file name
        file_exte = file[-3:] # Variable saves file extention
        print()
        print("*********************")
        print("Working on: " + file)

        ## Replacing all # in filename, because argument -s was passed.
        if len(argv) > 1:
            if argv[1] == "-s":
                file_name = file_name.replace("#", "")
            else:
            ## User passed argument that does not exist.
                print("No such argument. Continuing.")

        sorted_filename_length_dict, sub_folder_toggle, thumbs_db = engine.check_comic(file, file_name, file_exte) # Sends file for processing amd recieves sorted dictionary with diferent length filenames, sub_folder_toggle value and thumbs_db tuple.

        if sub_folder_toggle == 1:
            print("")
            print("!!!Detected a sub folder in archive file!!!")
            print("It will be removed if any images will be removed.")
            print("Comic will still work normaly.")
            print("")
        
        if thumbs_db[0] == 1:
            print("")
            print("!!!Detected a thumbs.db file in archive file!!!")
            print("It will be removed if any images will be removed.")
            print("Comic will still work normaly.")
            print("")
            delete_files.append(thumbs_db[1])

        user_promt_for_deletion()

        print("")

exit()