#! /usr/bin/python3
### Gui interface for comicAutoEditor writen in PyQt5

from sys import argv, exit

from os.path import expanduser, split

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton, QGroupBox, QCheckBox, QLineEdit, QTableWidget, QTableView, QFileDialog, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt

from engine import Engine
engine = Engine()

class ComicAutoEditorGui(QMainWindow):
    ## Main class that will have all the widgets for the program

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.center() # Centers (more or less) window in the screen on start up
        self.setWindowTitle("Comic Editor") # Setting window title
        main_widget = MainWidget(self) # Initiating QWidget that will be only window for this program
        self.setCentralWidget(main_widget) # Setting MainWidget as central widget for QMainWindow   
        self.show() # Displaying QMainWindow

    def center(self):
        # Copied this function from https://gist.github.com/saleph/163d73e0933044d0e2c4
        # Getting to lazy to research it myself.
        
        # geometry of the main window
        window_geometry = self.frameGeometry()

        # center point of screen
        center_point = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        window_geometry.moveCenter(center_point)

        # top left of rectangle becomes top left of window centering it
        self.move(window_geometry.topLeft())


class MainWidget(QWidget):

    def __init__(self, parent):
        ## Initiating MainWidget
        super(MainWidget, self).__init__(parent) ## I have no idea what kind of magic going on here
        
        self.init_variables()
        
        self.init_UI()

    def init_UI(self):
        ## Function that makes UI for the program
        layout = QGridLayout() # Setting QWidget layout to be grid

        ## All UI elemnts in order they are added
        ## Variable names are self explanatory
        self.label_filename = QLabel("No comic is selected")
        self.label_filename.setAlignment(Qt.AlignCenter)

        button_select_comic = QPushButton("Select Comic")
        button_select_comic.clicked.connect(self.choose_comic_file)

        page_filename_groupbox = QGroupBox("Page Filename")
        page_filename_groupbox_layout = QVBoxLayout()
        page_filename_remove_checkbox = QCheckBox("Remove")
        page_filename_remove_line_edit = QLineEdit()
        page_filename_remove_line_edit.setEnabled(False)
        page_filename_remove_line_edit.setPlaceholderText("Text you want to remove.")
        page_filename_replace_checkbox = QCheckBox("Replace with")
        page_filename_replace_line_edit = QLineEdit()
        page_filename_replace_line_edit.setEnabled(False)
        page_filename_replace_line_edit.setPlaceholderText("Text you want to replace with")
        page_filename_groupbox_layout.addWidget(page_filename_remove_checkbox)
        page_filename_groupbox_layout.addWidget(page_filename_remove_line_edit)
        page_filename_groupbox_layout.addWidget(page_filename_replace_checkbox)
        page_filename_groupbox_layout.addWidget(page_filename_replace_line_edit)
        page_filename_groupbox.setLayout(page_filename_groupbox_layout)

        self.comic_file_table = QTableWidget()
        self.comic_file_table.setColumnCount(2)
        self.comic_file_table.horizontalHeader().hide()
        self.comic_file_table.verticalHeader().hide()
        self.comic_file_table.resizeColumnToContents(0)
        self.comic_file_table.horizontalHeader().setStretchLastSection(True)

        self.button_convert_to_cbz = QPushButton("Convert to CBZ")
        self.button_convert_to_cbz.setToolTip("Will not change content of the archive.")
        self.button_convert_to_cbz.setEnabled(False)
        self.button_convert_to_cbz.clicked.connect(self.convert_to_cbz_clicked)

        self.button_remove_subfolder_thumbs = QPushButton("Remove Trash")
        self.button_remove_subfolder_thumbs.setToolTip("Only removes subfolder and thumbs.db in archive. Will not remove pages.")
        self.button_remove_subfolder_thumbs.setEnabled(False)
        self.button_remove_subfolder_thumbs.clicked.connect(self.button_remove_subfolder_thumbs_clicked)

        self.button_fix_comic = QPushButton("Fix Comic")
        self.button_fix_comic.setToolTip("Removes selected images, subfolder, thumbs.db and renames pages if chosen.")
        self.button_fix_comic.setEnabled(False)

        self.label_message = QLabel()
        self.label_message.setAlignment(Qt.AlignCenter)

        # Adding all UI elements to the layout
        layout.addWidget(self.label_filename, 0, 0, 1, 6)
        layout.addWidget(button_select_comic, 0, 6, 1, 1)
        layout.addWidget(page_filename_groupbox, 1, 0, 3, 7)
        layout.addWidget(self.comic_file_table, 5, 0, 8, 6)
        layout.addWidget(self.button_convert_to_cbz, 9, 6, 1, 1)
        layout.addWidget(self.button_remove_subfolder_thumbs, 10, 6 , 1, 1)
        layout.addWidget(self.button_fix_comic, 12, 6, 1, 1)
        layout.addWidget(self.label_message, 13, 0, 1, 7)
        self.setLayout(layout) # Setting layout the QMainWindow.

    def choose_comic_file(self):
        ## Prompts user to select a file and checks selected file. Set's variables used by other functions later.

        # chosen_file = QFileDialog.getOpenFileName(self, "Choose Comic File", expanduser("~"), "Comics (*.cbr *.cbz)")[0] # Prompts user to select comic file and saves result to variable
        chosen_file = QFileDialog.getOpenFileName(self, "Choose Comic File", expanduser("/mnt/Parsiusta/"), "Comics (*.cbr *.cbz)")[0] # Trinti
        
        if chosen_file != "": # Checks if user actually selected a file

            # Resetting all variables for new file
            self.init_variables()

            # Disabling all buttons for new file
            self.button_convert_to_cbz.setEnabled(False)
            self.button_remove_subfolder_thumbs.setEnabled(False)
            self.button_fix_comic.setEnabled(False)

            # Disabling connection to the table
            self.comic_file_table.disconnect()

            chosen_file_exte = split(chosen_file)[1][-4:].lower() # Saves user's chosen's file extention to a variable

            if chosen_file_exte == ".cbz" or chosen_file_exte == ".cbr":
                ## Checks if user's selected file actually ends with.
                ## Set's variables, shows message to user with file name and enables buttons if True
                self.comic_file = chosen_file
                self.comic_file_name = split(self.comic_file)[1][:-4]
                self.comic_file_exte = chosen_file_exte

                # Printin file that is being worked on.
                self.label_filename.setText(self.comic_file_name + self.comic_file_exte)

                self.label_message.clear() # Clears message in case user selected a not comic file previously or working with multiple file in a row.

                # Checking if comic arhcive is rar file. If true enabling "Convert to CBZ button"
                if self.comic_file_exte == ".cbr":
                    self.button_convert_to_cbz.setEnabled(True)

                # Getting more variables that will be used to by other functions. For more info check engine.check_comic.
                self.sorted_filename_length_dict, self.sub_folder_toggle, self.thumbs_db = engine.check_comic(self.comic_file, self.comic_file_name, self.comic_file_exte)

                # Enabling button "Remove Trash" if toggles are switched by check_engine funcktion
                if self.sub_folder_toggle == 1 or self.thumbs_db[0] == 1:
                    self.button_remove_subfolder_thumbs.setEnabled(True)
                
                # Enabling "Fix Comic" button
                self.button_fix_comic.setEnabled(True)

                self.label_message.clear() # Clears message in case user selected a not comic file previously or working with multiple file in a row.

                self.display_comic_files()

            else:
                ## Prints a message to user if he selected not comic file.
                self.label_message.setText("You have to select cbr or cbz file.")

    def display_comic_files(self):
    ## Adds all comic archive files to the QtableWidget and marks checkmarks as suggestion based on sorted_file_length_dict

        self.comic_file_list = engine.archive_file_list(self.comic_file, self.comic_file_name, self.comic_file_exte) # Getting archive's file list from engine.
        self.comic_file_table.setRowCount(len(self.comic_file_list)) # Setting tables row count to the count of files inside archive

        ## This makes two presumptions. First, is that first (shortest) file in dictionary will be the one that needs to be removed. Second, that it will be mention just once. Dictionary is already sorted by key (filename length) and this if statement checks if this length one found just once. Adding it to the delete_files list if true.
        if self.sorted_filename_length_dict[0][1][1] == 1:
            self.delete_files.append(self.sorted_filename_length_dict[0][1][0])

        ## If thumbs_db toggle is switched adding it to the delete file list.
        if self.thumbs_db[0] == 1:
            self.delete_files.append(self.thumbs_db[1])
      
        for item in range(len(self.comic_file_list)):
            ## Adding every item from archive to the table
            item_checkbox_detele = QTableWidgetItem()
            if self.comic_file_list[item] in self.delete_files:
                item_checkbox_detele.setCheckState(Qt.Unchecked) # Setting checkmark as Unchecked. Files is marked for deletion
            else:
                item_checkbox_detele.setCheckState(Qt.Checked)
            item_checkbox_detele.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled) # Checkmark's cell not editable, but state still can be changed.
            item_filename = QTableWidgetItem(split(self.comic_file_list[item])[1]) # Getting just a filename, without a path to the file in archive.
            item_filename.setFlags(Qt.ItemIsEnabled) # Filename's cell not editable
            self.comic_file_table.setItem(item, 0, item_checkbox_detele)
            self.comic_file_table.setItem(item, 1, item_filename)
        
        self.comic_file_table.cellChanged.connect(self.comic_file_table_cell_changed)

    def convert_to_cbz_clicked(self):
        ## This fuction exists because it is not possible to pass variables using connect
        engine.convert_to_cbz(self.comic_file, self.comic_file_name)
        self.label_message.setText("Converted " + self.comic_file_name + " to cbz")

    def button_remove_subfolder_thumbs_clicked(self):
        ## This function removes only subfolder and thumbs.db if they exists in the archive.
        ## Even if any other file will be selected for deletion it won't be deleted.
        
        local_delete_files = [] # Instead of global delete file, local one will be used.
        
        ## Adding thumbs.db to the delete list if it exists.
        if self.thumbs_db[0] == 1:
            local_delete_files.append(self.thumbs_db[1])
        
        engine.write_comic(self.comic_file, self.comic_file_name, self.comic_file_exte, local_delete_files, []) # Passing empty list for remove_from_filename. This function do not change filenames.

    def comic_file_table_cell_changed(self, row, column):
        ## Function triggred when user toggles checkmark in table.

        clicked_item_state = self.comic_file_table.item(row, column).checkState()
        clicked_item_filename = self.comic_file_list[row] # Gets filename for the checkmark from comic file list based on checkmark's row.
        
        ## Depending of the state of the checkmark checks if filename is marked for deletion. Depending on the that removes or adds filename to delete_list
        if clicked_item_state == Qt.Checked:
            if clicked_item_filename in self.delete_files:
                self.delete_files.remove(clicked_item_filename)
        elif clicked_item_state == Qt.Unchecked:
            if clicked_item_filename not in self.delete_files:
                self.delete_files.append(clicked_item_filename)

    def init_variables(self):
    ## Variables needed for Engine Functions
        self.comic_file = ""
        self.comic_file_name = ""
        self.comic_file_exte = ""
        self.sorted_filename_length_dict = dict()
        self.sub_folder_toggle = 0
        self.thumbs_db = (0, "")
        self.comic_file_list =[]
        self.delete_files = []
        self.remove_from_filename = []

if __name__ == "__main__":
    ComicAutoEditor = QApplication(argv)
    mainWindow = ComicAutoEditorGui()
    exit(ComicAutoEditor.exec_())