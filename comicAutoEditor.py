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

current_dir_files = listdir() # Getting all the filenames in current working dir

## Creates ~/Comics directory if it doesn't exits.
comic_save_location = expanduser("~") + "/Comics/" # Creating a path for the folder to create.
try:
    mkdir(comic_save_location)
except FileExistsError:
    # Folder already exists.
    pass

delete_files = [] # List containing all filenames to delete

for file in current_dir_files:
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

        sorted_filename_length_dict, sub_folder_toggle = engine.check_comic(file, file_name, file_exte) # Sends file for processing amd recieves sorted dictionary with diferent length filenames and sub_folder_toggle value

        ## Promts user to choose what file to delete, by printing sorted dictionary.
        print("Delete item:")
        for item in range(len(sorted_filename_length_dict)):
            print(str(item) + ". " + str(sorted_filename_length_dict[item][1][0]))
        if sub_folder_toggle == 1:
            print("v. Only Detele Subfolder")
        print("x. Skip")

        user_choice = input("[<ENTER> default = 0] ") # Saved user choise

        ## Sorting user choice.
        try:
            if user_choice.lower() == "x":
                print("Skipping")
                pass
            elif user_choice.lower() == "v":
                if sub_folder_toggle == 1:
                    # Detecting user choice to delete subfolder only. Passing empty sting as file that needs to be deleted. That way nothing matching will be found and only folder will be removed.
                    engine.write_comic(file, file_name, file_exte, delete_files, comic_save_location)
                else:
                    print("There is no such option for this file. Skipping to next step.")
            elif user_choice == "":
                # Detecting <ENTER>
                delete_files.append(sorted_filename_length_dict[0][1][0])
                print("Deleting: " + ", ".join(delete_files))
                engine.write_comic(file, file_name, file_exte, delete_files, comic_save_location)
            elif int(user_choice) in range(len(sorted_filename_length_dict)):
                # User's choice where he/she chose to file themselves.
                delete_files.append(sorted_filename_length_dict[int(user_choice)][1][0])
                print("Deleting: " + ", ".join(delete_files))
            else:
                # Not valid user input
                print("There is no such option. Skipping to next step.")
        except ValueError:
            print("There is no such option. Skipping to next step.")

exit()