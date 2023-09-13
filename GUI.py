##################################################################################################################################################################################
# Author: Jackson Sholdice, August 28th, 2023
# File contains all code related to building the automation GUI. 
##################################################################################################################################################################################

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTextEdit, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QListWidget
from PyQt5.QtGui import QIcon, QPalette, QFont, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt

import recipe_run

# set color template for all elements
class ColorPalette:
    def __init__(self):
        self.hover_color = "rgb(0, 175, 145)"
        self.background_color = "rgb(47, 46, 51)"
        self.text_color = "rgb(255, 255, 255)"
        self.field_color = self.background_color
        self.border_color = "rgb(255, 255, 255)"
        self.tab_color = "rgb(0, 115, 95)"
        self.selected_color = self.tab_color

# push button creater class
class PushButton(QPushButton, ColorPalette):
    def __init__(self, name, page, toggle_sequence_method = None, runner_sequence= False):
        super().__init__(name, page)
        self.state = 0  # intial state should be unpressed                                     
        
        self.toggle_sequence_method = toggle_sequence_method    # grab the toggle sequence function from main window 
        self.runner_sequence = runner_sequence                  # grab start runner flag, which will only be true when run sequence is pressed

        self.setStyleSheet(     # default button scheme 
            f"background-color: {self.background_color}; color: {self.text_color};"
            f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
        )
        
        self.enterEvent = self.on_hovered       # assigning the hovering method to the enter event attribute of the button 
        self.leaveEvent = self.on_left          # assign the left method to the leave event attribute of the button 
        self.clicked.connect(self.on_clicked)   # call the on clicked method when button is pressed    

    def on_hovered(self, event):    # when cursor hovers over button if unpressed change color scheme 
        self.setStyleSheet(
            f"background-color: {self.hover_color}; color: {self.text_color};"
            f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
        )

    def on_left(self, event):       # when cursor is no longer hovering over the button return to the default color scheme if unpressed 
        if self.state == 0:
            self.setStyleSheet(
                f"background-color: {self.background_color}; color: {self.text_color};"
                f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
            )
        if self.state == 1:
            self.setStyleSheet(
                f"background-color: {self.selected_color}; color: {self.text_color};"
                f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
            )

    def on_clicked(self):  
        if self.state == 0:     # if clicked and the button is off change to selected color scheme 
            self.setStyleSheet(
                f"background-color: {self.selected_color}; color: {self.text_color};"
                f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
            )
            self.state = 1      # set the button state to on 
        else:
            self.setStyleSheet( # if clicked and the button is on change to default color scheme
                f"background-color: {self.background_color}; color: {self.text_color};"
                f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
            )
            self.state = 0      # set the button state to off
   
        if self.runner_sequence:            # if run sequence flag is true then then toggle run sequence state (on if off and v.v.)
            self.toggle_sequence_method()

# class that handles program's print statements and emits signal to logging widget 
class LogStream:
    def __init__(self, signal):
        self.signal = signal
        self.buffer = ""        # initializes buffer to accumulate text

    def write(self, message):
        self.buffer += message                  # append new print statement to buffer
        if "\n" in self.buffer:                 # checks for new line character
            lines = self.buffer.split("\n")     # splits the buiffer into lines
            for line in lines[:-1]:             # emit each line using the singal, except the last line since it may be incomplete
                self.signal.emit(line)
            self.buffer = lines[-1]             # store last line in the buffer, since it may be incomplete 

class MainRunner(QThread):
    output_signal = pyqtSignal(str)     # defines output_signal as an emiiter with a string parameter

    def __init__(self, user_inputs, procedure_states, selected_software_tests):
        super().__init__()                                      # intialize recipe_run arguments
        self.user_inputs = user_inputs
        self.procedure_states = procedure_states
        self.selected_software_tests = selected_software_tests
        self.running = True

    def run(self):
        # Redirect stdout and stderr to the QTextEdit widget
        sys.stdout = LogStream(self.output_signal)
        sys.stderr = LogStream(self.output_signal)

        if self.running: # Call the main function from your other script
            recipe_run.main(self.user_inputs, self.procedure_states, self.selected_software_tests)





class MainWindow(QMainWindow, ColorPalette):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        font = QFont()
        font.setPointSize(10)
        QApplication.setFont(font)  # set default font size to size 9
        
        self.setWindowTitle("Otto")
        self.running = False    # initialize running state
        self.palette = ColorPalette()
        
        self.tab_widget = QTabWidget(self)  # create a tab widget
        self.main_page = QWidget()      # create two pages
        self.create_recipe = QWidget()

        ########## User input variable label and text fields ########## 
        self.ip_address_label = QLabel("Enfield IP Address:", self.main_page)
        self.ip_address_input = QLineEdit('000.000.000.000', self.main_page)    # default IP address for Alpha 1 (soon to be Beta 1...)
        self.ip_address_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")

        self.password_label = QLabel("VNC Password:", self.main_page)
        self.password_input = QLineEdit('0000', self.main_page)                 # default password for Alpha/Beta 1
        self.password_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")
        self.password_input.setEchoMode(QLineEdit.Password)     # the default will be 1234, but will appear as ****

        self.recipe_index_label = QLabel("Recipe Index (Unapproved):", self.main_page)
        self.recipe_index_input = QLineEdit('5', self.main_page)              # default recipe index for dilution run on nxgen 500 
        self.recipe_index_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")


        self.nxgen_label = QLabel("NxGen Mixer Type:", self.main_page)
        self.nxgen_input = QComboBox(self.main_page)                          # drop-down menu for nxgen mixer types
        self.nxgen_input.setStyleSheet(
            f"QComboBox {{ background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; padding: 2px; border-radius: 3px; }}"
            "QComboBox::drop-down { border: 0px; }"
            f"QComboBox QAbstractItemView {{ selection-background-color: {self.palette.hover_color}; selection-color: {self.palette.text_color} }}"  # Remove hover highlighting
        )

        self.nxgen_input.addItems([
            '500 GMP', 
            '500 Dilution GMP',
            '500 RUO',
            '500 Dilution RUO',
            '1000 GMP',
            '1000 Dilution GMP',
            '1000 RUO',
            '1000 Dilution RUO',
        ])
        # Retrieve the selected item text and set that as the primary text
        self.nxgen_input.setItemText(self.nxgen_input.currentIndex(), self.nxgen_input.currentText()) 

        self.batch_label_label = QLabel("Batch Label:", self.main_page)
        self.batch_label_input = QLineEdit('Test', self.main_page)                  # default batch label is test
        self.batch_label_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")

        self.flood_time_label = QLabel("Prime Flood Time [s]:", self.main_page)    
        self.flood_time_input = QLineEdit('1', self.main_page)                      # default manual flood time is 1s
        self.flood_time_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")

        self.flush_volume_label = QLabel("Uninstall Flush Volume [mL]:", self.main_page)
        self.flush_volume_input = QLineEdit('10', self.main_page)
        self.flush_volume_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")
        
        self.iteration_label = QLabel("Number of Iterations:", self.main_page)
        self.iteration_input = QLineEdit('2', self.main_page)
        self.iteration_input.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")
        


        ########### Procedure buttons ###########
        self.builder_label = QLabel("Sequence Builder", self.main_page)
        
        # create procedure buttons using PushButton builder class
        self.startup = PushButton("STARTUP", self.main_page)
        self.install = PushButton("INSTALL", self.main_page)
        self.skip_installation = PushButton("Skip Installation", self.main_page)
        self.start_batch = PushButton("START BATCH", self.main_page)
        self.prime = PushButton("PRIME", self.main_page)
        self.skip_prime = PushButton("Skip Prime", self.main_page)
        self.calibrate = PushButton("CALIBRATE", self.main_page)
        self.skip_calibrate = PushButton("Skip Calibrate", self.main_page)
        self.formulate = PushButton("FORMULATE", self.main_page)
        self.uninstall = PushButton("UNINSTALL", self.main_page)
        
        self.new_user_label = QLabel("First Time User", self.main_page)
        self.new_user_startup = PushButton("Initial Startup", self.main_page)      # initialize formulate button and signal

        self.run_button = PushButton("RUN SEQUENCE", self.main_page, self.toggle_run_sequence, runner_sequence=True)               # initialize run sequence button and signal
        
       
        ####################################################### SWTST SELECTION ############################################################################
        self.software_test_label = QLabel("Software Test Cases", self.main_page)
        self.software_test_input = QListWidget(self.main_page)    # create a list widget showing all software test cases                            
        self.software_test_input.setSelectionMode(QListWidget.MultiSelection)   # be able to select multiple test case
        software_tests= [                           # update list with complete software test cases                         
            'SWTST_348',
            'SWTST_272',
            'SWTST_273',
            'DVBM900'
        ]
        software_tests.sort()                       # display test cases alphabetically
        self.software_test_input.addItems(software_tests)
        # size the list widget depending on contents
        self.software_test_input.setFixedSize(self.software_test_input.sizeHintForColumn(0) + 2 * self.software_test_input.frameWidth() + 40, self.software_test_input.sizeHintForRow(0) * self.software_test_input.count() + 2 * self.software_test_input.frameWidth())
        self.software_test_input.setStyleSheet(
            f"QListWidget::item:selected{{background-color: {self.palette.selected_color}; color: {self.palette.text_color};}}"
            f"QListWidget::item:hover{{background-color: {self.palette.hover_color}; color: {self.palette.text_color};}}"
            f"QListWidget {{background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;}}"
        )
        self.software_test_input.setFocusPolicy(Qt.NoFocus) # removes border around last selected item 

        ########## Logging ##########
        self.log_text = QTextEdit(self.main_page)
        self.log_text.setFixedHeight(125)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(f"background-color: {self.palette.field_color}; border: 1px solid {self.border_color}; border-radius: 3px;")

        ########## Procedure button vertical layout ##########
        procedure_button_layout = QVBoxLayout()
        # organize subsequent buttons top to bottom 
        procedure_button_layout.addWidget(self.builder_label)
        procedure_button_layout.addWidget(self.startup)
        procedure_button_layout.addWidget(self.install)
        procedure_button_layout.addWidget(self.skip_installation)
        procedure_button_layout.addWidget(self.start_batch)
        procedure_button_layout.addWidget(self.prime)
        procedure_button_layout.addWidget(self.skip_prime)
        procedure_button_layout.addWidget(self.calibrate)
        procedure_button_layout.addWidget(self.skip_calibrate)
        procedure_button_layout.addWidget(self.formulate)
        procedure_button_layout.addWidget(self.uninstall)
        procedure_button_layout.addStretch(1)
        procedure_button_layout.setSpacing(20)


        ########## User input variable field vertical layout ##########
        user_input_layout = QVBoxLayout()
        # VNC related widgets
        user_input_layout.addWidget(self.ip_address_label)
        user_input_layout.addWidget(self.ip_address_input)
        user_input_layout.addSpacing(5)
        user_input_layout.addWidget(self.password_label)
        user_input_layout.addWidget(self.password_input)
        user_input_layout.addSpacing(5)
        # batch related widgets
        user_input_layout.addWidget(self.recipe_index_label)
        user_input_layout.addWidget(self.recipe_index_input)
        user_input_layout.addSpacing(5)
        user_input_layout.addWidget(self.nxgen_label)
        user_input_layout.addWidget(self.nxgen_input)
        user_input_layout.addSpacing(5)
        user_input_layout.addWidget(self.batch_label_label)
        user_input_layout.addWidget(self.batch_label_input)
        user_input_layout.addSpacing(5)
        user_input_layout.addWidget(self.iteration_label)
        user_input_layout.addWidget(self.iteration_input)
        user_input_layout.addSpacing(5)
        # unit procedure related widget
        user_input_layout.addWidget(self.flush_volume_label)
        user_input_layout.addWidget(self.flush_volume_input)
        user_input_layout.addSpacing(5)
        user_input_layout.addWidget(self.flood_time_label)
        user_input_layout.addWidget(self.flood_time_input)
        procedure_button_layout.addStretch(1)
        
        
        ########## Software test dropdown vertical layout ##########
        
        software_test_layout = QVBoxLayout()
        software_test_layout.addWidget(self.software_test_label)
        software_test_layout.addWidget(self.software_test_input)
        software_test_layout.addStretch(1)  # keeps label and input togteher at the top of the window
        software_test_layout.addWidget(self.new_user_label)
        software_test_layout.addWidget(self.new_user_startup)

        
        ########## Horizontal layout for user inputs and procedure buttons ##########
        # organize vertical layouts left to right 
        hbox_layout = QHBoxLayout()
        hbox_layout.addSpacing(10)
        hbox_layout.addLayout(user_input_layout)
        hbox_layout.addSpacing(60)
        hbox_layout.addLayout(procedure_button_layout)
        hbox_layout.addSpacing(60)
        hbox_layout.addLayout(software_test_layout)
        hbox_layout.addSpacing(10)

        grid_layout = QVBoxLayout(self.main_page)
        grid_layout.addLayout(hbox_layout)
        grid_layout.addSpacing(10)
        grid_layout.addWidget(self.log_text)
        grid_layout.addSpacing(10)
        grid_layout.addWidget(self.run_button)

        # add
        self.tab_widget.addTab(self.main_page, "Main Page")
        self.tab_widget.addTab(self.create_recipe, "Create Recipe")

        ########### Set the central widget ##########
        self.setCentralWidget(self.tab_widget) 
        self.tab_widget.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color}; ")

        # Set the stylesheet for the main window
        main_window_stylesheet = (
            f"QMainWindow {{ background-color: {self.palette.tab_color}; color: {self.palette.text_color}; }}"
            f"QTabWidget::pane {{ border: none; }}"  # Remove the border around the tab widget
            f"QTabBar::tab {{ background-color: {self.palette.tab_color}; padding: 8px; }}"
            f"QTabBar::tab:selected {{ border: 1px solid {self.palette.tab_color}; border-bottom-color: {self.palette.text_color}; color: {self.palette.text_color}; }}"
        )
        self.setStyleSheet(main_window_stylesheet)  
        self.setWindowIcon(QIcon("otto.png"))  # Clear any existing icon

        app_palette = QPalette()
        app_palette.setColor(QPalette.Highlight, QColor(0, 115, 95))
        QApplication.setPalette(app_palette)
        
        # self.move_to_top_right()

    ########## Run sequence function ##########
    def run_sequence(self):
        self.run_button.setText("SHUTDOWN SEQUENCE")    # toggle label of run sequence button 
        self.running = True                         # toggle running state 

        # get the values from the text inputs
        smartserver_ip = self.ip_address_input.text()
        smartserver_password = self.password_input.text()
        recipe_index = self.recipe_index_input.text()
        nxgen_label = self.nxgen_input.currentText()
        batch_label = self.batch_label_input.text()
        flood_time = self.flood_time_input.text()
        flush_volume = self.flush_volume_input.text()
        n_iteration = self.iteration_input.text()

        # specify path to SmartClient app
        smartclient_path = "SmartClient_V17.exe"
        # initial set point for the display scaling algorithm to math the original screen scaling
        initial_display_scale = '61'

        # nxgen size dictionary for service page selection 
        nxgen_dict = {
            '500 GMP': 0,
            '500 Dilution GMP': 1,
            '500 RUO': 2,
            '500 Dilution RUO': 3,
            '1000 GMP': 4,
            '1000 Dilution GMP': 5,
            '1000 RUO': 6,
            '1000 Dilution RUO': 7
        }
        nxgen = nxgen_dict[nxgen_label] # given user input the nxgen value will store the position of that specified label in the drop down table on the service page

        # create list iteratively assigning the text from the selected software test 
        selected_software_tests = [item.text() for item in self.software_test_input.selectedItems()]

        # compress user input arguments
        user_inputs = (
            initial_display_scale, smartclient_path, smartserver_ip, smartserver_password, 
            nxgen, recipe_index, batch_label, flood_time, flush_volume, int(n_iteration)
        )
        # compress procedure states into 1 argument
        procedure_states = [
            self.new_user_startup.state, self.startup.state, self.install.state, self.skip_installation.state, 
            self.start_batch.state, self.prime.state, self.skip_prime.state, 
            self.calibrate.state, self.skip_calibrate.state, self.formulate.state, self.uninstall.state
        ]

        self.log_text.clear()
        # create instsance of MainRunner that will update the logs 
        self.main_runner = MainRunner(user_inputs, procedure_states, selected_software_tests)
        self.main_runner.output_signal.connect(self.update_log)
        self.main_runner.finished.connect(self.stop_sequence)

        self.main_runner.start()    # run the main runner class to begin recipe_run

    def toggle_run_sequence(self):
        if not self.running:
            self.run_sequence()
        else:
            raise SystemError

    def stop_sequence(self):
        self.running = False
        self.run_button.setText("RUN SEQUENCE") # toggle sequence button back to run 
        self.run_button.setStyleSheet(          # return to default button scheme 
            f"background-color: {self.background_color}; color: {self.text_color};"
            f"border: 1px solid {self.border_color}; border-radius: 3px; padding: 4px 8px;"
        )
        self.run_button.state = 0
    
    # update the log widget with new print statements recieved during runtime
    def update_log(self, message):
        self.log_text.append(message)
    
    '''
    def move_to_top_right(self):
        # Get the user's screen geometry
        screen_geometry = QDesktopWidget().screenGeometry()
        window_width = self.geometry().width()
        window_height = self.geometry().height()

        # Calculate the top right position
        top_right_x = screen_geometry.width() - window_width
        top_right_y = 0
        
        self.move(top_right_x, top_right_y)  # Move the window to the top right
    '''
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
