##################################################################################################################################################################################
# Author: Jackson Sholdice, August 28th, 2023
# File contains prcoessing function that reads and executes unit procedure sequences and unit procedure tests. 
##################################################################################################################################################################################

import os 
import time
import threading 
import pyautogui as pg

import Helper_Functions
import Sequence_Instructions

import HMI_Image_Library
service = HMI_Image_Library.Service()
system_state = HMI_Image_Library.System_State()

# calculates region of HMI screen to search for on the users display 
left, top, width, height  = Helper_Functions.get_HMI_region()

# set timeout durations for searching for buttons, default is short 
short_timeout = 120
long_timeout = 1000
no_timeout = 12000

####################################################################################################
# PRIMARY PROGRAM FUNCTIONS
####################################################################################################
def procedure_processing(sequence, time_delay=1, timeout = short_timeout):
    i = 0   # initialize index
    next_item_1 = True                                                          # initialize next item, default is the normal tuple (image, action)
    next_item_2 = False                                                         # initialize conditional item, (default image, default action, possible image, corresponding possible action)
    logged_out = pg.locateOnScreen(system_state.logged_out, confidence=0.95)    # check if logged out
    
    if logged_out:                                          # if state is currently in logged out mode
        login = Sequence_Instructions.login_sequence()  
        sequence = login + sequence                         # push login sequence to the top of the list of instructions before carrying out original sequence
    
    for elements in sequence:                               # iterate over every element (tuple) in sequence
        # in some cases 2 buttons could be possible depending on system's state, must check which possible button was found when the confirm next button was executed 
        if next_item_1:                                     # checks if the default button was found 
            item, instructions = elements[0], elements[1]   # assigns the first two default values of the tuple
        elif next_item_2:                                   # checks if the alternative button was found 
            item, instructions = elements[2], elements[3]   # assigns the alternative image path and respective action

        if i != len(sequence) - 1:                                          # checks if the current element is not the last element in sequence
            if len(sequence[i + 1]) > 2:                                    # if the next tuple has an alternative possible button 
                next_item = [sequence[i + 1][0], sequence[i + 1][2]]        # grab the default image path and the alternative image path 
            else: 
                next_item = [sequence[i + 1][0]]            # if not only grab the normal default button path 
        else:
            next_item = False                               # if the current element is the last element then assign next item as false 

        try:
            timer = threading.Timer(timeout, timeout_handler)   # create timer instance that will raise systemexit error if button not detected
            timer.start()                                       # start timer
            if time_delay:                                      # time delay is set to True
                next_item_1, next_item_2 = run_procedure(item, instructions, next_item, time_delay)        # by default run_procedure
            else:
                print('Entering speed run procedure, there will be no navigation prints in the following sequence')
                speed_run_procedure(item, instructions, next_item, time_delay)  # use run_procedure with no time delays for SWTST that require rapid step execution 
            timer.cancel()                                      # end timer
        except Exception as e:                                  # if exception is raise dy timeout_handler 
            timer.cancel()
            raise e                                             # exit out of sequence 
        
        i += 1    

def timeout_handler():
    print('Timeout Error: Could not detect button')
    raise SystemExit

# organizing function used to determine path for png or text item, call button finding function, call next button finding function, and organize print statements to user
def run_procedure(item, instructions, next_item, time_delay, confidence=0.95):
    if item.endswith('.png'):                                                               # if the item is a button image
        current_icon = os.path.splitext(os.path.basename(item))[0]                          # separates base name of image from the whole path and removes the .png file extension
        find_button(item, *instructions, time_delay=time_delay, confidence=confidence)      # finds the current button and will execute respective iunstruction set
        print('Found current icon: ' + str(current_icon))
    else:                                                           # if the item is screen text
        find_text(item, *instructions, time_delay=time_delay)       # search for the given text
        print('Found current text: ' + str(item))  
    next_item_1, next_item_2 = True, False
    
    if next_item:                   # checks that the current step is not the last in the sequence
        if len(next_item) > 1:      # checks if there is multiple possible next buttons  
            next_icon_1 = os.path.splitext(os.path.basename(next_item[0]))[0]       # separates base name for both images from the whole path and removes the .png file extension
            next_icon_2 = os.path.splitext(os.path.basename(next_item[1]))[0]
            print('Searching for next icon: ' + str(next_icon_1) + ' and ' + str(next_icon_2))
            next_item_1, next_item_2 = confirm_next_button(next_item, confidence)   # search for both buttons and return a true or false statement attached to each possible button
            if next_item_1:                                      
                print('Found next icon: ' + str(next_icon_1))                       # print which button was found
            else:
                print('Found next icon: ' + str(next_icon_2))
            
        else:                                                                       # if there is only one possible next button than continue as normal 
            if next_item[0].endswith('.png'):                                       # if the next item is a button image
                next_icon = os.path.splitext(os.path.basename(next_item[0]))[0]     # separates base name of image from the whole path and removes the .png file extension
                print('Searching for next icon: ' + str(next_icon))
                confirm_button_change(next_item[0], confidence)             # confirms that the next button appears after instructions were executed on current button, once proven program can move on
                print('Found next icon: ' + str(next_icon) + '\n')
            else:                                                           # if the next item is a screen text
                print('Searching for next text: ' + str(next_item[0]))
                confirm_screen_change(next_item[0])                         # confirms that the next text appears after instructions were executed on current button, once proven program can move on
                print('Found next text: ' + str(next_item[0]) + '\n')

    return next_item_1, next_item_2

# identical to run_procedure, except it does not output print statements and there are no time delays
def speed_run_procedure(item, instructions, next_item, time_delay, confidence=0.95):
    if item.endswith('.png'):                                                           # if the item is a button image
        find_button(item, *instructions, time_delay=time_delay, confidence=confidence)  # finds the current button and will execute respective iunstruction set
    else:                                                                               # if the item is screen text
        find_text(item, *instructions, time_delay=time_delay)                           # search for the given text
        
    if next_item:                                               # checks that the instruction in sequence is not the last
        if next_item[0].endswith('.png'):                       # if the next item is a button image
            confirm_button_change(next_item[0], confidence)     # confirms that the next button appears after instructions were executed on current button, once proven program can move on
        else:                                                   # if the next item is a screen text
            confirm_screen_change(next_item[0])                 # confirms that the next text appears after instructions were executed on current button, once proven program can move on

# waits for specific text to appear on screen before executing a set of instructions
def find_text(screen, *instructions, time_delay):
    text = []
    while screen not in text:                                           # continue searching until text is found
        text = Helper_Functions.extract_text()
    for instruction in instructions:
        time.sleep(time_delay)
        instruction(screen)                                             # iteratively execute action out of the instruction set

# confirm the appearance of the next text
def confirm_screen_change(next_screen):
    while next_screen not in Helper_Functions.extract_text():           # wait until the next text is eventually found
        None

# waits for a specific window or button to appear and then will execute a set of instructions
def find_button(image_path, *instructions, time_delay, confidence):
    button = False
    while not button:                                                   # keep searching until button is found
        button = pg.locateOnScreen(image_path, confidence=confidence, region=(left, top, width, height))
    for instruction in instructions:                                    # once image is found execute instructions given in the lambda function
        time.sleep(time_delay)
        instruction(button)

# Confirm the appearance of the next button
def confirm_button_change(image_path, confidence):
    while not pg.locateOnScreen(image_path, confidence=confidence, region=(left, top, width, height)): # continually check for next button to appear before moving on to next step of procedure
        None

def confirm_next_button(next_item, confidence):
    item_1 = False
    item_2 = False
    while not item_1 and not item_2:
        item_1 = pg.locateOnScreen(next_item[0], confidence=confidence)
        item_2 = pg.locateOnScreen(next_item[1], confidence=confidence)
    return item_1, item_2


#####################################################################################################
# UNIT PROCEDURE FUNCTIONS
#####################################################################################################
# run when the its the first time a user is using the program
def first_start_up(smartclient_path, smartserver_ip, smartserver_password, initial_display_scale):
    print("INITIALIZING...")
    os.startfile(smartclient_path)                          # open the smartclient application
    Sequence_Instructions.first_start_up_sequence(smartserver_ip, smartserver_password, initial_display_scale)
    time.sleep(5)
    Helper_Functions.display_scale(initial_display_scale)   # find scale factor for users laptop that will resize the button icons to fit their screen resolution
    print("INITIALIZING COMPLETE")

# Start-up SmartClient program, login to HMI, and navigates to the home page 
def start_up(smartclient_path, smartserver_ip, smartserver_password):
    os.startfile(smartclient_path)
    Sequence_Instructions.start_up_sequence(smartserver_ip, smartserver_password)

# login sequence
def login():
    procedure_processing(Sequence_Instructions.login_sequence())

# sets the nxgen size set by user at the top of the code 
def NxGen(nxgen):
    procedure_processing(Sequence_Instructions.nxgen_sequence(nxgen))

# nav to service page, skip fluid path installation, and nav back to home
def skip_installation():
    procedure_processing(Sequence_Instructions.skip_installation_sequence())

# nav to service page, skip fluid path prime, and nav back to home
def skip_prime():
    procedure_processing(Sequence_Instructions.skip_prime_sequence())

# nav to service page, skip flow meter calibration, and nav back to home
def skip_calibration():
    procedure_processing(Sequence_Instructions.skip_calibration_sequence())

def install():
    procedure_processing(Sequence_Instructions.install_sequence(), timeout = long_timeout)

# create new recipe from scratch 
def new_recipe(recipe_name, recipe_description, nxgen, volume, flowrate, a_ratio, b_ratio, dil_ratio, reagent_ratio):
    procedure_processing(Sequence_Instructions.new_recipe_dil_sequence(recipe_name, recipe_description, nxgen, volume, flowrate, a_ratio, b_ratio, dil_ratio, reagent_ratio))

# starts a new batch from home page given a specific recipe index 
def start_batch(nxgen, batch_label, recipe_index):
    procedure_processing(Sequence_Instructions.nxgen_sequence(nxgen))
    procedure_processing(Sequence_Instructions.start_batch_sequence(batch_label, recipe_index))

# starts a priming sequence depending on seleceted mixer type
def start_priming(nxgen, flood_time):
    if nxgen % 2 == 1:  # checks to see if the nxgen is odd (all odd values for nxgen use dilution line C)
        procedure_processing(Sequence_Instructions.priming_with_dil_sequence(flood_time), timeout=long_timeout)
    else:
        procedure_processing(Sequence_Instructions.priming_no_dil_sequence(flood_time), timeout=long_timeout)

# starts calibration from home page, will walk through recipe that does not require manual intervention  
def start_calibration(nxgen):
    if nxgen % 2 == 1:  # checks to see if the nxgen is odd (all odd values for nxgen use dilution line C)
        procedure_processing(Sequence_Instructions.calibration_with_dil_sequence(), timeout=long_timeout)
    else:
        procedure_processing(Sequence_Instructions.calibration_no_dil_sequence(), timeout=long_timeout)

# starts formulating from home page and will complete batch after formulatio then return to the home page
def start_formulation():
    procedure_processing(Sequence_Instructions.formulation_sequence(), timeout=no_timeout)

# starts the uninstall unit procedure with a user specified flush volume for both lines (currently setup for only flushing lines A/B)
def start_uninstall(flush_volume):
    procedure_processing(Sequence_Instructions.uninstall_sequence(flush_volume))

#####################################################################################################
# SOFTWARE TEST FUNCTIONS
#####################################################################################################
def start_SWTST_348(flood_time):
    print('RUNNING SWTST_348')
    initial_test_sequence, final_test_sequence = Sequence_Instructions.SWTST_348(flood_time)
    # TODO: need this step to be faster and more reliable, currently must use e-stop physically
    #procedure_processing(initial_test_sequence, time_delay=0)   # need the initial fail operation step to move quicker than normal or else it won't fail in time to trigger alarm
    procedure_processing(final_test_sequence, timeout=long_timeout)                   # the rest of the test will execute at a normal pace to prevent possibility of failure
    print('SUCCESSFULLY COMPLETED SWTST_348')  

def start_SWTST_272():
    print('RUNNING SWTST_272')
    initial_test, final_test = Sequence_Instructions.SWTST_272()
    procedure_processing(initial_test, timeout=no_timeout)
    procedure_processing(final_test, time_delay=0)
    print('SUCCESSFULLY COMPLETED SWTST_272')

def start_SWTST_273():
    print('RUNNING SWTST_273')
    procedure_processing(Sequence_Instructions.SWTST_273(), timeout=no_timeout)
    print('SUCCESSFULLY COMPLETED SWTST_273')

def DVBM900(nxgen, batch_label, recipe_index, flood_time, flush_volume, n_iteration):
    print("RUNNING DVBM900 FOULING TEST")
    procedure_processing(Sequence_Instructions.cumulative_sequence(nxgen, batch_label, recipe_index, flood_time, flush_volume, n_iteration))
    print("SUCCESSFULLY COMPLETED DVBM900 FOULING TEST")

