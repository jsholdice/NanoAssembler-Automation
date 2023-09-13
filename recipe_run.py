##################################################################################################################################################################################
# Author: Jackson Sholdice, August 28th, 2023
# File contains code related to calling unit prcoedure/ software test functions. 
##################################################################################################################################################################################

import Sequence_Functions

####################################################################################################
# MAIN FUNCTION
####################################################################################################
def main(user_inputs, procedure_states, selected_software_tests):

    # decompress user inputs
    (initial_display_scale, smartclient_path, smartserver_ip, smartserver_password,
     nxgen, recipe_index, batch_label, flood_time, flush_volume, n_iteration) = user_inputs

    # store sequences as a list which will be called when the corresponding button is pressed
        # stores the function and arguments separtely as tuples
    sequence_functions = [
        (Sequence_Functions.first_start_up,(smartclient_path, smartserver_ip, smartserver_password, initial_display_scale)),
        (Sequence_Functions.start_up, (smartclient_path, smartserver_ip, smartserver_password)),
        (Sequence_Functions.install, ()),
        (Sequence_Functions.skip_installation, ()),
        (Sequence_Functions.start_batch, (nxgen, batch_label, recipe_index)),
        (Sequence_Functions.start_priming, (nxgen, flood_time)),
        (Sequence_Functions.skip_prime, ()),
        (Sequence_Functions.start_calibration, [nxgen]),
        (Sequence_Functions.skip_calibration, ()),
        (Sequence_Functions.start_formulation, ()),
        (Sequence_Functions.start_uninstall, [flush_volume]),
        (Sequence_Functions.new_recipe, ())
    ]

    # dictionary of software tests that can be called when the key is passed 
    software_tests_dict = {
        'SWTST_348': (Sequence_Functions.start_SWTST_348, [flood_time]),
        'SWTST_272': (Sequence_Functions.start_SWTST_272, ()),
        'SWTST_273': (Sequence_Functions.start_SWTST_273, ()),
        'DVBM900': (Sequence_Functions.DVBM900, (nxgen, batch_label, recipe_index, flood_time, flush_volume, n_iteration))
    } 

    # iterate through selected procedures in a sequential way 
    for index, procedure_state in enumerate(procedure_states):
        if procedure_state: # if the procedure state is pressed, set to 1 (True) 
            func, args = sequence_functions[index]  # grab function and arguments from tuple
            func(*args)     # calls function with all arguments

    # iterate through all selected software tests if selected 
    for software_test in selected_software_tests:   
        func, args = software_tests_dict[software_test] # grab function and respective arguments from tuple
        func(*args)         # calls function with all arguments 
