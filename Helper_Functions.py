##################################################################################################################################################################################
# Author: Jackson Sholdice, August 28th, 2023
# File contains functions related to intial start up for new user. 
# Also contains functions to find text on screen, scale image library scale if there is a screen resolution problem (scaling does not work for small screen, resize image library, be wary of commits with new scaled image library)
##################################################################################################################################################################################


import os 
from PIL import Image
from PIL import ImageGrab
import pyautogui as pg
import time
import win32api
import win32con
import win32gui
import pytesseract

import HMI_Image_Library
service = HMI_Image_Library.Service()
system_state = HMI_Image_Library.System_State()
start_connection = HMI_Image_Library.Start_Connection()

original_x = 586        # original width and height of the HMI screen on original screen captured screen 
original_y = 1074

# determine the scaling factor required to resize the icon image specific to the users computer to ensure program is searching for an appropriate resolute icon
def image_scale(original_x=586, original_y=1074):
    # take screenshot of image
    screenshot = ImageGrab.grab()
    # Get the user's screen size
    screen_width, screen_height = screenshot.size

    # Calculate the starting position at the center of the screen
    start_x = screen_width // 2
    start_y = screen_height // 2
    # initialize the half height variables
    half_y = 0
    half_x = 0
    pixel_colour = screenshot.getpixel((start_x, start_y))   # stores pixel colour value at the given position
    # move pixel by pixel across the screen until black boarder is reached and record the half width pixel count
    while pixel_colour != (0,0,0) and half_x < start_x - 1: # stop once at black border or when out of index of the screen
        half_x += 1
        pixel_colour = screenshot.getpixel((start_x + half_x, start_y))

    pixel_colour = screenshot.getpixel((start_x, start_y))
    # move pixel by pixel down the screen until black boarder is reached and record the half height pixel count
    while pixel_colour != (0,0,0) and half_y < start_y - 1: # stop once at black border or when out of index of the screen
        half_y += 1
        pixel_colour = screenshot.getpixel((start_x, start_y + half_y))

    # calculate conversion factor from original icon resolution to the current user's required icon resoltuion
    x_scale = (2*half_x)/original_x
    y_scale = (2*half_y)/original_y
    print('x scale: ' + str(x_scale) + ' y scale: ' + str(y_scale))

    return x_scale, y_scale

# scale the hmi screen to a size that aligns with the HMI_Image_Library icon sizings 
def display_scale(initial_display_scale):
    print('\n' + 'Scaling Screen...')
    
    x_scale, y_scale = image_scale()                            # determine the current image scaling 
    increase_display_scale_percent = int(initial_display_scale) # initialize the display scale percentage to the original default of 61%
    decrease_display_scale_percent = int(initial_display_scale) # initialize the display scale percentage to the original default of 61%

    while (x_scale or y_scale) > 1.01 or (x_scale or y_scale) < 0.99:   # if the scaling factor of the hmi_screen is too large relative to the original screen than iterate until it is within range
        if (x_scale or y_scale) < 0.99:                         # if the scaling factor is too low
            increase_display_scale_percent += 1                 # increase the display screen size
            set_display_scale(increase_display_scale_percent)   # set this increased display screen size
            time.sleep(1)                                       # time delay neccessary since the options screen will still be visible when program goes to count pixels in the image scale function
            x_scale, y_scale = image_scale()                    # calculate new hmi_screen scaling 
        
        elif (x_scale or y_scale) > 1.01:                       # if scaling factor of the hmi_screen is too high 
            decrease_display_scale_percent -= 1                 # decrease the display screen size
            set_display_scale(decrease_display_scale_percent)   # set this decreased display screen size 
            time.sleep(1)                                       # time delay neccessary since the options screen will still be visible when program goes to count pixels in the image scale function
            x_scale, y_scale = image_scale()                    # caluclate the new hmi_screen scaling

    return x_scale, y_scale     # once hmi screen scaling is within reasonable bounds, return this scaling values

# function called to change the current display scale on the hmi_panel
def set_display_scale(display_scale_percent):
    pg.hotkey('ctrl','alt','shift','o')         # nav to options screen
    time.sleep(0.3)
    pg.press('tab', presses=7)                  # tab to display scale field
    time.sleep(0.3)
    pg.typewrite(str(display_scale_percent))    # type desired scaling factor
    time.sleep(0.3)
    pg.press('enter')                           # enter factor and return to main screen
    time.sleep(0.3)

# given image path, resizes to match users display, may no longer need this 
def resize_image_library(hmi_image_library_path, x_scale, y_scale):
    # Iterate over subfolders in the given folder path
    for root, dirs, files in os.walk(hmi_image_library_path):
        # Exclude the start_up icons from resizing since these screens do not scale with increasing screen size
        if start_connection.path in dirs:
            dirs.remove(start_connection.path)
        
        for file in files:
            # Check if the file is a PNG image
            if file.lower().endswith('.png'):
                # Get the full path of the image file
                image_path = os.path.join(root, file)
                
                # Resize the image
                resized_image = resize_image(image_path, x_scale, y_scale)

                # Save the resized image, overwriting the original file
                resized_image.save(image_path)

# function to resize individual images
def resize_image(image_path, x_scale, y_scale):
    # Open the image using PIL/Pillow
    image = Image.open(image_path)
                
    # Calculate the new dimensions
    new_width = int(image.width * x_scale)
    new_height = int(image.height * y_scale)
                
    # Resize the image
    resized_image = image.resize((new_width, new_height),Image.BILINEAR)

    return resized_image

# returns all the text on the current window screen 
def extract_text():
    active_window_handle = win32gui.GetForegroundWindow()       # Get the handle of the active window
    window_rect = win32gui.GetWindowRect(active_window_handle)  # Get the bounding box of the active window
    screenshot = ImageGrab.grab(window_rect)                    # Capture the screenshot of the active window

    text = pytesseract.image_to_string(screenshot)              # Perform OCR on the screenshot image
    return(text)

# checks if a display device is the main monitor (primary display)
def is_main_monitor(display_device):
    return display_device.StateFlags & win32con.DISPLAY_DEVICE_PRIMARY_DEVICE != 0

# gets the main monitor's DeviceName (unique identifier)
def get_main_monitor():
    monitors = []
    try:
        i = 0
        while True:     # enumerate through all display devices
            display_device = win32api.EnumDisplayDevices(None, i)
            if display_device.StateFlags & win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP:     # checks if the display device is attached to the desktop
                monitors.append(display_device)                                             # adds the attached monitor to the list
            i += 1
    except win32api.error:
        pass

    for monitor in monitors:            # check if any of the attached monitors is the main monitor
        if is_main_monitor(monitor):
            return monitor.DeviceName   # return the DeviceName of the main monitor

    return None

# gets the dimensions (width and height) of the main monitor
def get_HMI_region():
    main_monitor = get_main_monitor()
    if main_monitor:                            # retrieve the current display settings of the main monitor
        devmode = win32api.EnumDisplaySettings(main_monitor, win32con.ENUM_CURRENT_SETTINGS)
        screen_width = devmode.PelsWidth        # get the screen width in pixels
        screen_height = devmode.PelsHeight      # get the screen height in pixels
        return int(screen_width/2 - original_x/2), int(screen_height/2 - original_y/2), int(original_x), int(original_y)  # return region of HMI screen converted to integers
    else:
        return None

# TO DO: after run sequence is pressed go to home and check state of the system, if the state is beyond the selected unit procedure nav to service and align unit procedure with user selected procedure
def check_system_state():
    system_state_options = [system_state.logged_out,                        # list of possible states depicted on the unit procedure process workflow on the home page
                            system_state.install, 
                            system_state.batch_plan, 
                            system_state.prime, 
                            system_state.calibrate,
                            system_state.formulate, 
                            system_state.formulate_complete, 
                            system_state.uninstall]
    current_state = [0, 0, 0, 0, 0, 0, 0, 0]                                # initialize states

    system_state_page = pg.locateOnScreen(service.home, confidence=0.95)    # search for home button 
    if system_state_page:                                                   # if home button can be found (won't be found if startup hasn't occured)
        pg.click(system_state_page)                                         # click home button 
        for index, system_state_option in enumerate(system_state_options):  # iterate through states and search for a match 
            if pg.locateOnScreen(system_state_option, confidence=0.99):
                current_state[index] = 1                                    # if there is a match flip the corresponding state bit
    print(current_state)
    return current_state
'''
# Looks for two buttons and executes a command based on which one is found first 
def find_two_buttons(image_path1, image_path2, commands_button1, commands_button2):
    button1 = None
    button2 = None
    
    while not button1 and not button2:  # search for both buttons
        button1 = pg.locateOnScreen(image_path1, confidence=confidence)
        button2 = pg.locateOnScreen(image_path2, confidence=confidence)
    
    if button1:  # only button1 is found
        for command in commands_button1:    # execute command associated with button 1
            command(button1)
    else:  # only button2 is found 
        for command in commands_button2:    # execute command associated with button 2
            command(button2)

# searhces for all buttons with the same icon and then will execute commands on the button specified via the location argument (default -> first found)
def find_all_button(image_path, location = 0, *commands):
    buttons = pg.locateAllOnScreen(image_path, confidence=confidence)   # search for the given image
    if not buttons:                                                     # likely won't find button immediately
        while not buttons:                                              # keep searching until button is found
            buttons = pg.locateOnScreen(image_path, confidence=confidence)
        for command in commands:               # once image is found execute commands given in the lambda function
            command(buttons[location])
    else:                                      # if found immediately, execute commands
        for command in commands:
            command(buttons[location])

# may not be of use, it seems as though the smartclient start up screen does not scale with different screen resolutions
def start_up_scaling():
    # initialize scaling factors
    scale_down = 1.00
    scale_up = 1.00
    
    # Load the original image
    satellite = pg.locateOnScreen(start_connection.new_connection, confidence=0.8)

    # Iterate until the image is found
    while not satellite:
        # Scale down the image by 1%
        scale_down *= 0.99
        print("scaling: " + str(scale_down))
        upscale_satellite = resize_image(start_connection.new_connection, scale_down, scale_down)
    
        # Search for the resized image on the screen
        satellite = pg.locateOnScreen(upscale_satellite, confidence=0.8)
    
        if not satellite:
            # Scale up the image by 1%
            scale_up *= 1.01
            print("scaling: " + str(scale_up))
            downscale_satellite = resize_image(start_connection.new_connection, scale_up, scale_up)
        
            # Search for the resized image on the screen
            satellite = pg.locateOnScreen(downscale_satellite, confidence=0.8)
    
    if abs(scale_down - 1) > abs(scale_up - 1):
        print("satellite found!")
        resize_image_library(start_connection.path, scale_down, scale_down)
    else:
        print("satellite found!")
        resize_image_library(start_connection.path, scale_up, scale_up)
'''