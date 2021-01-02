#! /usr/bin/python3
### Gui interface for comicAutoEditor writen in PyQt5

from sys import argv, exit

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton, QGroupBox, QCheckBox, QLineEdit, QTableWidget, QTableView
from PyQt5.QtCore import Qt

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
        self.init_UI()

    def init_UI(self):
        ## Function that makes UI for the program
        layout = QGridLayout() # Setting QWidget layout to be grid

        ## All UI elemnts in order they are added
        ## Variable names are self explanatory
        label_filename = QLabel("No comic is selected")
        label_filename.setAlignment(Qt.AlignCenter)

        button_select_comic = QPushButton("Select Comic")

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

        archive_file_list = QTableWidget()
        archive_file_list.setColumnCount(2)
        archive_file_list.horizontalHeader().setStretchLastSection(True)

        # tool_tip_button_convert_to_cbz = QToolTip("Will not change content to of the archive")
        button_convert_to_cbz = QPushButton("Convert to CBZ")
        button_convert_to_cbz.setToolTip("Will not change content to of the archive.")
        button_convert_to_cbz.setEnabled(False)

        button_remove_subfolder_thumbs = QPushButton("Remove trash")
        button_remove_subfolder_thumbs.setToolTip("Only removes subfolder and thumbs.db in archive. Will not remove pages.")
        button_remove_subfolder_thumbs.setEnabled(False)

        button_fix_comic = QPushButton("Fix comic")
        button_fix_comic.setToolTip("Removes selected images, subfolder, thumbs.db and renames pages if chosen.")
        button_fix_comic.setEnabled(False)

        label_message = QLabel()

        # Adding all UI elements to the layout
        layout.addWidget(label_filename, 0, 0, 1, 6)
        layout.addWidget(button_select_comic, 0, 6, 1, 1)
        layout.addWidget(page_filename_groupbox, 1, 0, 3, 7)
        layout.addWidget(archive_file_list, 5, 0, 8, 5)
        layout.addWidget(button_convert_to_cbz, 10, 6, 1, 1)
        layout.addWidget(button_remove_subfolder_thumbs, 11, 6 , 1, 1)
        layout.addWidget(button_fix_comic, 12, 6, 1, 1)
        layout.addWidget(label_message, 13, 0, 1, 7)
        self.setLayout(layout) # Setting layout the QMainWindow.



if __name__ == "__main__":
    ComicAutoEditor = QApplication(argv)
    mainWindow = ComicAutoEditorGui()
    exit(ComicAutoEditor.exec_())