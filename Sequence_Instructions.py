##################################################################################################################################################################################
# Author: Jackson Sholdice, August 28th, 2023
# File contains lists building up unit procedures with indicvidual (image, action) steps. 
##################################################################################################################################################################################

import time
import os
import pyautogui as pg
import pygetwindow as gw


#####################################################################################################
# IMPORT HMI BUTTON LIBRARIES
#####################################################################################################
import HMI_Image_Library
start_connection = HMI_Image_Library.Start_Connection()
system_state = HMI_Image_Library.System_State()
install = HMI_Image_Library.Install()
start_recipe = HMI_Image_Library.Start_Recipe()
service = HMI_Image_Library.Service()
controls = HMI_Image_Library.Controls()
prime = HMI_Image_Library.Prime()
calibrate = HMI_Image_Library.Calibrate()
formulate = HMI_Image_Library.Formulate()
create_recipe = HMI_Image_Library.Create_Recipe()
uninstall = HMI_Image_Library.Uninstall()

#####################################################################################################
# START UP PROCEDURE INSTRUCTIONS
#####################################################################################################
def first_start_up_sequence(smartserver_ip, smartserver_password, initial_display_scale):
    title_windows = [
        'New Sm@rtserver Connection',
        'Standard VNC Authentication',
        'hmi_panel',
        'Smartclient Options',
        'Sm@rtClient full-screen mode'
    ]

    window_instructions = [
        [lambda arg: pg.typewrite(smartserver_ip), lambda arg: pg.press('enter')],
        [lambda arg: pg.typewrite(smartserver_password), lambda arg: pg.press('enter')],
        [lambda arg: pg.hotkey('ctrl','alt','shift','o')],
        [lambda arg: pg.press('tab', presses=7),                 # tab to display scale field
            lambda arg: pg.typewrite(initial_display_scale),     # set display scale to the default of 61% (this is because 61% was the original scale and most moniotrs should be close to this)
            lambda arg: pg.press('tab', presses=2),              # tab to suppress device layout field
            lambda arg: pg.press('space'),                       # uncheck the box
            lambda arg: pg.press('enter'),                       # executes the suppression of the device layout by tabing to specific button
            lambda arg: pg.hotkey('ctrl','alt','shift','f')],
        [lambda arg: pg.press('enter')]
    ]

    for target_title, instruction in zip(title_windows, window_instructions):   # iterates over the title windows and corresponding instruction set 
        found = False                                                           # reset found flag       
        time.sleep(1)                                                           # will go very fast without delay, works but delay included for user to see the individual steps
        while not found:
            all_titles = gw.getAllTitles()
            for title in all_titles:                                            # iterate over all titles found
                if target_title in title:                                       # if there is a match execute instruction on target window     
                    print(f"found current screen: {target_title}")
                    window = pg.getWindowsWithTitle(target_title)[0]            # selects the window with the target title 
                    window.activate()                                           # ensures you are active on the desired window
                    for action in instruction:
                        arg = None                                              # enables lambda function to work
                        action(arg)                                             # Execute pyautogui function
                    found = True                                                # set found flag to true to escape while loop
                    break                                                       # Exit the for loop once a match is found

def start_up_sequence(smartserver_ip, smartserver_password):
    title_windows = [
        'New Sm@rtserver Connection',
        'Standard VNC Authentication',
        'hmi_panel',
        'Sm@rtClient full-screen mode'
    ]

    window_instructions = [
        [lambda arg: pg.typewrite(smartserver_ip), lambda arg: pg.press('enter')],
        [lambda arg: pg.typewrite(smartserver_password), lambda arg: pg.press('enter')],
        [lambda arg: pg.hotkey('ctrl','alt','shift','f')],
        [lambda arg: pg.press('enter')]
    ]

    for target_title, instruction in zip(title_windows, window_instructions):   # iterates over the title windows and corresponding instruction set 
        found = False                                                           # reset found flag       
        time.sleep(1)                                                           # will go very fast without delay, works but delay included for user to see the individual steps
        while not found:
            all_titles = gw.getAllTitles()
            for title in all_titles:                                            # iterate over all titles found
                if target_title in title:                                       # if there is a match execute instruction on target window     
                    print(f"found current screen: {target_title}")
                    window = pg.getWindowsWithTitle(target_title)[0]            # selects the window with the target title 
                    window.activate()                                           # ensures you are active on the desired window
                    for action in instruction:
                        arg = None                                              # enables lambda function to work
                        action(arg)                                             # Execute pyautogui function
                    found = True                                                # set found flag to true to escape while loop
                    break                                                       # Exit the for loop once a match is found

def login_sequence():
    login_sequence = [
        (system_state.logged_out, [lambda button: pg.click(button)]),
        (system_state.confirm_login, [lambda button: pg.click(button)]),
    ]
    return login_sequence

#####################################################################################################
# SERVICE PROCEDURE INSTRUCTIONS
#####################################################################################################
def nxgen_sequence(nxgen):
    # list of tuples containing buttons and respective actions to select the desired nxgen mixer specified by the user input variable nxgen
    nxgen_sequence = [
        (service.serv, [lambda button: pg.click(button)]),  # nav to service screen
        (service.nxgen, [                                   
            lambda button: pg.click(button),                # click NxGen drop down menu
            lambda button: pg.press('up', presses=8),       # presses up 8 times to get to the top selectable mixer and then moves down known amount
            lambda button: pg.press('down', presses=nxgen), # move down to selected mixer type
            lambda button: pg.press('enter')                # enter mixer type
        ]),
        (service.home, [lambda button: pg.click(button)])   # nav back to home
    ]
    return nxgen_sequence

def skip_installation_sequence():
    # list of tuples containing buttons and respective actions to set fluid path as installed upon start-up
    skip_installation_sequence = [
        (service.serv, [lambda button: pg.click(button)]),          # nav to service screen
        (service.set_installed, [lambda button: pg.click(button)]), # set fluid path installed
        (service.home, [lambda button: pg.click(button)])           # nav back to home
    ]
    return skip_installation_sequence

def skip_prime_sequence():
    # list of tuples containing buttons and respective actions to skip prime unit procedure
    skip_prime_sequence = [
        (service.serv, [lambda button: pg.click(button)]),          # nav to service screen
        (service.set_primed, [lambda button: pg.click(button)]),    # set fluid path to primed
        (service.home, [lambda button: pg.click(button)])           # nav back to home
    ]
    return skip_prime_sequence

def skip_calibration_sequence():
    # list of tuples containing buttons and respective actions to skip the calibration unit procedure
    skip_calibration_sequence = [
        (service.serv, [lambda button: pg.click(button)]),              # nav to service page
        (service.set_calibrated, [lambda button: pg.click(button)]),    # set fluid path to calibrated
        (service.home, [lambda button: pg.click(button)])               # nav to home
    ]
    return skip_calibration_sequence

#####################################################################################################
# UNIT PROCEDURE INSTRUCTIONS
#####################################################################################################
def install_sequence():
    install_sequence = [
        (install.install, [lambda button: pg.click(button)]),
        (install.start_install, [lambda button: pg.click(button)]),
        (install.skip_rfid, [lambda button: pg.click(button)]),
        (install.confirm, [lambda button: pg.click(button)]),
        (install.done, [lambda button: pg.click(button)]),
    ]
    return install_sequence

def new_recipe_no_dil_sequence(recipe_name, recipe_description, nxgen, volume, flowrate, a_ratio, b_ratio):
    new_recipe_no_dil = [                                             
        (create_recipe.recipes, [lambda button: pg.click(button)]),
        (create_recipe.create_new, [lambda button: pg.click(button)]),
        (create_recipe.next, [lambda button: pg.click(button)]), 
        (create_recipe.fluid_path, [lambda button: pg.click(button)]),    
        (create_recipe.next, [lambda button: pg.click(button)]),  
        (create_recipe.formulation, [lambda button: pg.click(button)]),
        (create_recipe.next, [lambda button: pg.click(button)]), 
        (create_recipe.viscosity, [lambda button: pg.click(button)]),     
        (create_recipe.next, [lambda button: pg.click(button)]),     
        (create_recipe.flow_monitoring, [lambda button: pg.click(button)]), 
        (create_recipe.next, [lambda button: pg.click(button)]),
        (create_recipe.name, [lambda button: pg.click(button),
                              lambda button: pg.typewrite(recipe_name),
                              lambda button: pg.press('enter', presses=2)]), 
        (create_recipe.description, [lambda button: pg.click(button),
                              lambda button: pg.typewrite(recipe_description),
                              lambda button: pg.hotkey('enter')]), 
        (create_recipe.nxgen, [lambda button: pg.click(button),
                               lambda button: pg.press('up', presses=2),
                               lambda button: pg.press('down', presses=nxgen),
                               lambda button: pg.press('enter')]),
        (create_recipe.use_dilution, [lambda button: pg.click(button)]), 
        (create_recipe.volume, [lambda button: pg.click(button),
                               lambda button: pg.typewrite(volume),
                               lambda button: pg.press('enter')]),
        (create_recipe.flow, [lambda button: pg.click(button),
                               lambda button: pg.typewrite(flowrate),
                               lambda button: pg.press('enter')]),
        (create_recipe.line_a, [lambda button: pg.click(button),
                               lambda button: pg.typewrite(a_ratio),
                               lambda button: pg.press('enter')]),
        (create_recipe.line_b, [lambda button: pg.click(button),
                               lambda button: pg.typewrite(b_ratio),
                               lambda button: pg.press('enter')]),
        (create_recipe.done, [lambda button: pg.click(button)]),
        (create_recipe.clear_filters, [lambda button: pg.click(button)]),
        (service.home, [lambda button: pg.click(button)]),    
    ]
    return new_recipe_no_dil

def new_recipe_dil_sequence(recipe_name, recipe_description, nxgen, volume, flowrate, a_ratio, b_ratio, dil_ratio, reagent_ratio):
    new_recipe_no_dil = new_recipe_no_dil_sequence(recipe_name, recipe_description, nxgen, volume, flowrate, a_ratio, b_ratio)
    del new_recipe_no_dil[14]

    dilutent = [
        (create_recipe.dilutent, [lambda button: pg.click(button),
                               lambda button: pg.typewrite(dil_ratio),
                               lambda button: pg.press('enter')]),
        (create_recipe.reagent, [lambda button: pg.click(button),
                               lambda button: pg.typewrite(reagent_ratio),
                               lambda button: pg.press('enter')]),
    ]

    new_recipe_dil = new_recipe_no_dil[:18] + dilutent + new_recipe_no_dil[18:]
    return new_recipe_dil

def start_batch_sequence(batch_label, recipe_index):
    # list of tuples containing buttons and respective actions to start a batch, 
        # give it the user-inputted name, and the desired batch index corresponding to a specific recipe
    start_batch_sequence = [
        (start_recipe.setup_batch, [lambda button: pg.click(button)]),  # enter setup batch page
        (start_recipe.unreleased_off, [lambda button: pg.click(button)], start_recipe.unreleased_on, [lambda button: pg.click(button)]),    # keep or turn on the unreleased button
        (start_recipe.batch_label, [lambda button: pg.click(button),
                                    lambda button: pg.typewrite(batch_label),
                                    lambda button: pg.press('enter')]),  # select batch label field and enter user-inputed name
        (start_recipe.recipe_index, [lambda button: pg.doubleClick(button),
                                    lambda button: pg.typewrite(recipe_index),
                                    lambda button: pg.press('enter')]),  # select recipe index field and enter user-input
        (start_recipe.start_batch, [lambda button: pg.click(button)]),      
        (start_recipe.next, [lambda button: pg.click(button)]),
        (start_recipe.flow_kit, [lambda button: pg.click(button)]),
        (start_recipe.next, [lambda button: pg.click(button)]),
        (start_recipe.formulation, [lambda button: pg.click(button)]),
        (start_recipe.next, [lambda button: pg.click(button)]),
        (start_recipe.viscosity, [lambda button: pg.click(button)]),
        (start_recipe.next, [lambda button: pg.click(button)]),
        (start_recipe.monitoring, [lambda button: pg.click(button)]),
        (start_recipe.next, [lambda button: pg.click(button)]),
        (start_recipe.review, [lambda button: pg.click(button)]),   
        (start_recipe.done, [lambda button: pg.click(button)]), 
        (start_recipe.home, [lambda button: pg.click(button)])              # nav back to home
    ]
    return start_batch_sequence

def priming_with_dil_sequence(flood_time):
    # call priming events
    start_prime, input_prime, end_prime = prime_events(flood_time)
    # combine priming events for a no dilution priming sequence
    priming_sequence = start_prime + input_prime + input_prime + input_prime + end_prime
    
    return priming_sequence

def priming_no_dil_sequence(flood_time):
    # call priming events
    start_prime, input_prime, end_prime = prime_events(flood_time)
    # combine priming events for a no dilution priming sequence
    priming_sequence = start_prime + input_prime + input_prime + end_prime

    return priming_sequence

def prime_events(flood_time):
    start_prime = [                                             # start prime sequence
        (prime.prime, [lambda button: pg.click(button)]),       # enter prime unit procedure                  
        (prime.start_prime, [lambda button: pg.click(button)]), # start prime
    ]

    input_prime = [
        (prime.prime_icon, [lambda button: pg.click(button)]),              # move cursor out of the way 
        (prime.continue_prime, [lambda button: pg.click(button)]),          # continue prime on line A
        (prime.start_manual_flood, [lambda button: pg.click(button),        # start manual flood
                                    lambda button: time.sleep(int(flood_time))]),# flood time sets the amount of time the manual flood is on for
        (prime.prime_icon, [lambda button: pg.click(button)]),              # move cursor out of the way
        (prime.stop_manual_flood, [lambda button: pg.click(button)]),       # stop the manual flood
        (prime.continue_prime, [lambda button: pg.click(button)]),          # click continue prime
        (prime.prime_icon, [lambda button: pg.click(button)]),              
        (prime.continue_prime, [lambda button: pg.click(button)]),          # click continue prime again
        (prime.prime_icon, [lambda button: pg.click(button)]),      
        (prime.continue_prime, [lambda button: pg.click(button)]),          # click continue prime again
    ]

    end_prime = [                                               # end prime sequence 
        (prime.verify_icon, [lambda button: pg.click(button)]), # move cursor 
        (prime.confirm, [lambda button: pg.click(button)]),     # confirm verification completed
        (prime.done_icon, [lambda button: pg.click(button)]),   # wait for the done icon to appear
        (prime.done, [lambda button: pg.click(button)])         # finish prime procedure
    ]

    return start_prime, input_prime, end_prime

def calibration_with_dil_sequence():
    calibration_no_dilution = calibration_no_dil_sequence() # obtains calibration sequence without diluition line
    # additional steps to be inserted into the priming sequence
    dilution_steps = [
        (calibrate.calibration_complete, [lambda button: pg.click(button)]),    # move cursor
        (calibrate.ready, [lambda button: pg.click(button)])                    # begin cal on line C
    ]
    calibration_sequence = calibration_no_dilution[:2] + dilution_steps + calibration_no_dilution[2:]   # insert dilution steps
    return calibration_sequence

def calibration_no_dil_sequence():
    # list of tuples containing buttons and respective actions to run a calibration
    calibration_sequence = [
        (calibrate.calibrate, [lambda button: pg.click(button)]),               # enter calibration unit procedure
        (calibrate.start_calibrate, [lambda button: pg.click(button)]),         # start calibration
        (calibrate.calibration_complete, [lambda button: pg.click(button)]),    # move cursor off ready button location such that the 98% confidence is not obscured by cursor
        (calibrate.ready, [lambda button: pg.click(button)]),                   # begin cal on line A
        (calibrate.calibration_complete, [lambda button: pg.click(button)]),    # move cursor
        (calibrate.ready, [lambda button: pg.click(button)]),                   # begin cal on line B
        (calibrate.verifying, [lambda button: pg.click(button)]),               # move cursor to verifying bubbles such that it off of the next button location
        (calibrate.done, [lambda button: pg.click(button)])                     # complete calibration procedure
    ]
    return calibration_sequence

def formulation_sequence():
    # list of tuples containing buttons and respective actions to run a formulation
    formulation_sequence = [
        (formulate.formulation, [lambda button: pg.click(button)]),         # nav to formulate unit procedure
        (formulate.start_formulation, [lambda button: pg.click(button)]),   # start formulation
        (formulate.no_comment, [lambda button: pg.click(button)]),                # wait for formulation to complete (the OK button will appear upon completion)
        (formulate.complete_batch, [lambda button: pg.click(button)]),      # press the complete batch button
        (formulate.next, [lambda button: pg.click(button)]),        # confirm completion
        (formulate.next, [lambda button: pg.click(button)]),           # click done 
        (formulate.save, [lambda button: pg.click(button)]),
        (formulate.done_batch, [lambda button: pg.click(button)]),
        (formulate.home, [lambda button: pg.click(button)])
    ]
    return formulation_sequence

def uninstall_sequence(flush_volume):
    uninstall_sequence = [
        (uninstall.uninstall, [lambda button: pg.click(button)]),
        (uninstall.start_uninstall, [lambda button: pg.click(button)]),
        (uninstall.flush_line, [lambda button: pg.click(button),
                                lambda button: pg.press('up', presses=3),
                                lambda button: pg.press('enter')]),
        (uninstall.flush_volume, [lambda button: pg.click(button),
                                  lambda button: pg.typewrite(flush_volume),
                                  lambda button: pg.press('enter')]),
        (uninstall.run_flush, [lambda button: pg.click(button)]),
        (uninstall.flushing, [lambda button: pg.click(button)]),
        (uninstall.run_flush, [lambda button: None]),
        (uninstall.flush_line, [lambda button: pg.click(button),
                                lambda button: pg.press('down'),
                                lambda button: pg.press('enter')]),
        (uninstall.flush_volume, [lambda button: pg.click(button),
                                  lambda button: pg.typewrite(flush_volume),
                                  lambda button: pg.press('enter')]),
        (uninstall.run_flush, [lambda button: pg.click(button)]),
        (uninstall.flushing, [lambda button: pg.click(button)]),
        (uninstall.run_flush, [lambda button: None]),
        (uninstall.next, [lambda button: pg.click(button)]),
        (uninstall.disconnect, [lambda button: pg.click(button)]),
        (uninstall.next, [lambda button: pg.click(button)]),
        (uninstall.run_drain, [lambda button: pg.click(button)]),
        (uninstall.disconnect, [lambda button: pg.click(button)]),
        (uninstall.stop_drain, [lambda button: pg.click(button)]),
        (uninstall.next, [lambda button: pg.click(button)]),
        (uninstall.removal, [lambda button: pg.click(button)]),
        (uninstall.next, [lambda button: pg.click(button)]),
        (uninstall.done_point, [lambda button: pg.click(button)]),
        (uninstall.done, [lambda button: pg.click(button)]),
    ]
    return uninstall_sequence

def cumulative_sequence(nxgen, batch_label, recipe_index, flood_time, flush_volume, n_iteration):
    # obtain sequences required to iterate through one-full run 
    installation = install_sequence()
    set_nxgen = nxgen_sequence(nxgen)
    start_batch = start_batch_sequence(batch_label, recipe_index)        
    priming_no_dilution = priming_no_dil_sequence(flood_time)          
    calibration_no_dilution = calibration_no_dil_sequence()            
    formulation = formulation_sequence()
    uninstall = uninstall_sequence(flush_volume)

    # group one run start to finish under an initial run and then repeat n times 
    initial_run  = installation + set_nxgen + start_batch + priming_no_dilution + calibration_no_dilution + formulation + uninstall
    
    # remove redudant typewrite steps when starting batch and uninstalling since these values carry over from last run and since typewrite will occasionally miss type on following runs 
    del start_batch[2:4]
    uninstall = uninstall[:3] + uninstall[4:8] + uninstall[9:]

    following_run = installation + start_batch + priming_no_dilution + calibration_no_dilution + formulation + uninstall    # removed nxgen step since it carries over from initial run 
    following_run = following_run * (n_iteration - 1)   # subtract by one due to initial run 
    complete_run = initial_run + following_run          # concatentae initial and following into one complete run 
    return complete_run

#####################################################################################################
# SOFTWARE TEST PROCEDURES
#####################################################################################################
# fail all operations in prime
def SWTST_348(flood_time):
    priming_no_dilution = priming_no_dil_sequence(flood_time)           # obtain normal priming sequence
    fail_operation_steps = fail_operation_sequence(prime.exit_prime, prime.home_confirm)    # fail operation given exit button and confriming no flush or formulation on home page

    tare_steps = [
        (prime.taring_flow_meter, [lambda button: pg.click(button)])    # steps to ensure taring screen appears during prime sequence so that alarm can be raised during tare
    ]
    
    # TO DO: to not hard code 5, 12 into sequence I could iterate over priming_no_dil_sequence until prime.start_manual_flood is reached
            # this would be robust against changes in the priming sequence, but not against a changing of the name convention.
    initial_test_sequence = (
        priming_no_dilution[:2] + fail_operation_steps                # raise alarm when FMs are being set up (commented out since it is too fast of an operation)
    )

    final_test_sequence = (
        priming_no_dilution[:5] + fail_operation_steps +                # raise alarm during manual flood
        priming_no_dilution[:12] + fail_operation_steps +               # raise alarm during pull flood
        priming_no_dilution[:12] + tare_steps + fail_operation_steps    # raise alarm during FM tare
    )   
    return initial_test_sequence, final_test_sequence

# run calibrate and fail each operation 
def SWTST_272():
    calibration_no_dilution = calibration_no_dil_sequence()             # obtain normal calibration sequence with no dilution line
    fail_operation_steps = fail_operation_sequence(calibrate.exit_calibrate, calibrate.home_confrim)    # fail operation given exit button and confriming no flush or formulation on home page
    calibrating = [(calibrate.calibrating_text, [lambda button: None])]   # wait until the calibrating text appears
    verification = [(calibrate.verification_text, [lambda button: None])]             # wait until the verifying text appears
    
    fail_operation_steps = fail_operation_sequence(calibrate.exit_calibrate, calibrate.home_confrim)    # fail operation given exit button and confriming no flush or formulation on home page
    
    interrupt_flow_1 = valve_state_sequence(controls.valve_f, controls.open_off)          # switch valves such that fluid flows through valve F, thus missing corioilis
    interrupt_flow_1 += valve_state_sequence(controls.valve_g, controls.closed_off)[1:]   # this will cause cal to fail since line fm and cal fm will disagree

    manual_flood_troubleshoot = calibration_troubleshoot_sequence(calibrate.use_manual_flood )      # manual flood troubleshooting method when cal fails 
    verify_viscosity_troubleshoot = calibration_troubleshoot_sequence(calibrate.verify_viscosity)   # verify viscosity troubleshooting method when cal fails

    initial_test_sequence = (
        #calibration_no_dilution[:2] + calibrating + fail_operation_steps +  
        #calibration_no_dilution[:6] + verification + fail_operation_steps +
        #calibration_no_dilution[:2] + calibrating + interrupt_flow_1 + manual_flood_troubleshoot + fail_operation_steps  
    )   
    # splitting up test sequence so that spped_run_procedure can be run on the final test sequence (need quick button pushes to get from set viscosity to service screen to cause error in time)   
    final_test_sequence = calibration_no_dilution[:2] + calibrating + verify_viscosity_troubleshoot + fail_operation_steps    # no need for interrupt_flow step since valves are already in correct state
    
    return initial_test_sequence, final_test_sequence

# run calibrate stopping each operation and continuing
def SWTST_273():
    calibration_no_dilution = calibration_no_dil_sequence()             # obtain normal calibration sequence with no dilution line
    stop_start_calibration = [(calibrate.stop, [lambda button: print('PASSED: operation stop screen appeared'),
                                                lambda button: pg.click(button)]),    # stop operation
                              (calibrate.continue_calibrate, [lambda button: pg.click(button)]),  # continue operation
                              (calibrate.ready, [lambda button: pg.click(button)])]  # restart operation

    stop_start_verification = [(calibrate.stop, [lambda button: print('PASSED: operation stop screen appeared'),
                                                 lambda button: pg.click(button)]),    # stop operation
                              (calibrate.continue_calibrate, [lambda button: pg.click(button)])]

    test_sequence = (
        calibration_no_dilution[:2] + stop_start_calibration +    # stop calibration operation on line A 
        calibration_no_dilution[2:4] + stop_start_calibration +   # stop calibration operation on line B
        calibration_no_dilution[4:7] + stop_start_verification +  # stop verification operation
        calibration_no_dilution[6:]                               # complete calibration
    )
    return test_sequence


#####################################################################################################
# SOFTWARE TEST HELPER FUNCTIONS
#####################################################################################################
# fail operations steps to be used in SWTST execution
def fail_operation_sequence(exit_button, test_confirmation):
    fail_operation_steps = [
        (service.serv, [lambda button: pg.click(button)]),              # nav to service screen
        (service.disabled_off, [lambda button: pg.click(button)]),      # disable RFID reader to raise alarm 
        (exit_button, [lambda button: print('PASSED: Error Message Appeared')]),
        (exit_button, [lambda button: pg.click(button)]),          # leave alarm page
        (test_confirmation, [lambda button: print('PASSED: Returned to home and no option to run flush or formulation')]),
        (service.serv, [lambda button: pg.click(button)]),              # nav back to service screen
        (service.enabled_off, [lambda button: pg.click(button)]),       # enable RFID reader to return to operating state
    ]
    return fail_operation_steps

# changes flow rate of a specified pump, assumes pump is currently in auto state
def manual_flow_sequence(pump_selection, flowrate):
    manual_flow_steps = [
        (controls.controls, [lambda button: pg.click(button)]),             # nav to controls screen
        (pump_selection, [lambda button: pg.click(button)]),                # select pump
        (controls.manual_off, [lambda button: pg.click(button)]),           # switch to manual
        (controls.start_pump, [lambda button: pg.press('tab', presses=4),   # waits for start pump button then tabs to flow rate
                               lambda button: pg.typewrite(str(flowrate)),  # enters flow rate
                               lambda button: pg.press('enter')]),
        (controls.start_pump, [lambda button: pg.click(button)]),
        (controls.close, [lambda button: pg.click(button)])                 # exits pump page
    ]
    return manual_flow_steps

# change state of specific valve, assuming valve is in auto state
def valve_state_sequence(valve_selection, valve_state, control_state = controls.manual_off):
    valve_state_steps = [
        (controls.controls, [lambda button: pg.click(button)]),     # nav to controls screen
        (valve_selection, [lambda button: pg.click(button)]),       # select valve
        (control_state, [lambda button: pg.click(button)]),         # switch to manual
        (valve_state, [lambda button: pg.click(button)]),           # select valve state
        (controls.close, [lambda button: pg.click(button),          # exits pump page
                          lambda button: print("Wait 2 minutes for calibration to fail")])         
    ]
    return valve_state_steps

# calibration troubleshooting sequence, given method you want to try 
def calibration_troubleshoot_sequence(troubleshoot_method):
    if troubleshoot_method == calibrate.use_manual_flood:   # if manual flood trouble shooting method is selected
        troubleshoot_steps = [
            (calibrate.troubleshoot, [lambda button: pg.click(button)]),        # click troubleshoot
            (calibrate.use_manual_flood, [lambda button: pg.click(button)]),    # click manual flood
            (calibrate.start_manual_flood, [lambda button: pg.click(button)])   # start the manual flood
        ]
    else:                                                   # if verify viscosity trouble shooting method is selected
        troubleshoot_steps = [
            (calibrate.troubleshoot, [lambda button: pg.click(button)]),        # click troubleshoot
            (calibrate.verify_viscosity, [lambda button: pg.click(button)]),    # click verify viscosity
            (calibrate.set_viscosity, [lambda button: pg.click(button)])        # set the viscosity 
        ]
    return troubleshoot_steps
