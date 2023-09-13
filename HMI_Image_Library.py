##################################################################################################################################################################################
# Author: Jackson Sholdice, August 28th, 2023
# File contains button paths to the HMI folder for the respective unit procedure. 
##################################################################################################################################################################################

import os 

current_directory = os.path.dirname(os.path.abspath(__file__))
target_folder = "enfield_hmi_remote_control"

path_parts = current_directory.split(os.path.sep)
index = path_parts.index(target_folder) + 1

base_path = os.path.sep.join(path_parts[:index])

#####################################################################################################
# SEQUENCE PROCEDURE BUTTON CLASSES
#####################################################################################################

# class containing the button template paths to connect to the HMI via SmartClient
class Start_Connection:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Start_Connection\\'
        self.new_connection = 'New Sm@rtserver Connection'
        self.authentication = 'Standard VNC Authentication'
        self.hmi_panel = 'hmi'
        self.fullscreen_mode = 'Sm@rtClient full-screen mode'
        self.smartclient_options = 'Smartclient Options'
        self.home = self.path + 'home.png'

class Install:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Install\\'
        self.install = self.path + 'install.png'
        self.start_install = self.path + 'start_install.png'
        self.installing = self.path + 'installing.png'
        self.skip_rfid = self.path + 'skip_rfid.png'
        self.verifying = self.path + 'verifying.png'
        self.confirm = self.path + 'confirm.png'
        self.ok = self.path + 'ok.png'
        self.done = self.path + 'done.png'
        self.password = self.path + 'password.png'


# class containing the button template paths for starting a recipe 
class Start_Recipe:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Start_Recipe\\'
        self.setup_batch = self.path + 'setup_batch.png'
        self.unreleased_on = self.path + 'unreleased_on.png'
        self.unreleased_off = self.path + 'unreleased_off.png'
        self.released_on = self.path + 'released_on.png'
        self.released_off = self.path + 'released_off.png'
        self.start_batch = self.path + 'start_batch.png'
        self.verify_recipe  = self.path + 'verify_recipe.png'
        self.home = self.path + 'home.png'
        self.batch_label = self.path + 'batch_label.png'
        self.recipe_index = self.path +'recipe_index.png'
        self.next = self.path + "next.png"
        self.flow_kit = self.path + "flow_kit.png"
        self.formulation = self.path + "formulation.png"
        self.viscosity = self.path + 'viscosity.png'
        self.monitoring = self.path + 'monitoring.png'
        self.review = self.path + 'review.png'
        self.done = self.path + 'done.png'
 
# class containing the button template paths related to the service page
class Service:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Service\\'
        self.serv = self.path + 'service.png'
        self.set_installed = self.path + 'set_installed.png'
        self.set_primed = self.path + 'set_primed.png'
        self.set_calibrated = self.path + 'set_calibrated.png'
        self.set_formulation_complete = self.path + 'set_formulation_complete.png'
        self.home = self.path + 'home.png'
        self.nxgen = self.path + 'nxgen.png'
        self.disabled_off = self.path + 'disabled_off.png'
        self.enabled_off = self.path + 'enabled_off.png'

# class containing the button templates related to the controls page
class Controls:
    def __init__(self):
        self.path = base_path + 'HMI_Buttons\\Controls\\'
        self.controls = self.path + 'controls.png'
        
        self.pump_a = self.path + 'pump_a.png'
        self.pump_b = self.path + 'pump_b.png'
        self.pump_c = self.path + 'pump_c.png'
        self.pump_p = self.path + 'pump_p.png'
        
        self.manual_off = self.path + 'manual_off.png'
        self.manual_on = self.path + 'manual_on.png'
        self.auto_on = self.path + 'auto_on.png'
        self.auto_off = self.path + 'auto_off.png'
        self.flow_on = self.path + 'flow_on.png'
        self.speed_off = self.path + 'speed_off.png'
        self.start_pump = self.path + 'start_pump.png'
        
        self.flow_a = self.path + 'flow_a.png'
        self.flow_b = self.path + 'flow_b.png'
        self.flow_c = self.path + 'flow_c.png'
        self.cal_fm = self.path + 'cal_fm.png'
        
        self.valve_a = self.path + 'valve_a.png'
        self.valve_b = self.path + 'valve_b.png'
        self.valve_c = self.path + 'valve_c.png'
        self.valve_d = self.path + 'valve_d.png'
        self.valve_e = self.path + 'valve_e.png'
        self.valve_f = self.path + 'valve_f.png'
        self.valve_g = self.path + 'valve_g.png'

        self.open_on = self.path + 'open_on.png'
        self.open_off = self.path + 'open_off.png'
        self.closed_on = self.path + 'closed_on.png'
        self.closed_off = self.path + 'closed_off.png'

        self.close = self.path + 'close.png'
        
# class containing button template paths necceesary for the priming sequence
class Prime:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Prime\\'
        self.prime = self.path + 'prime.png'
        self.start_prime = self.path + 'start_prime.png'
        self.prime_icon = self.path + 'prime_icon.png'
        self.continue_prime = self.path + 'continue_prime.png'
        self.start_manual_flood = self.path + 'start_manual_flood.png'
        self.stop_manual_flood = self.path + 'stop_manual_flood.png'
        self.stop = self.path + 'stop.png'
        self.verify_icon = self.path + 'verify_icon.png'
        self.confirm = self.path + 'confirm.png'
        self.done_icon = self.path + 'done_icon.png'
        self.done = self.path + 'done.png'
        self.exit_prime = self.path + 'exit_prime.png'
        self.drawing_fluid = self.path + 'drawing_fluid.png'
        self.taring_flow_meter = self.path + 'taring_flow_meter.png'
        self.home_confirm = self.path + 'SWTST_348_confirm_home.png'

# class containing the button template paths for calibration 
class Calibrate:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Calibrate\\'
        self.calibrate = self.path + 'calibrate.png'
        self.start_calibrate = self.path + 'start_calibrate.png'
        self.calibration_complete = self.path + 'calibration_complete.png'
        self.ready = self.path + 'ready.png'
        self.calibrate_complete = self.path + 'calibrate_complete.png'
        self.verifying = self.path + 'verifying.png'
        self.done = self.path + 'done.png'
        self.done_adjust_off = self.path + 'done_adjust_off.png'
        self.calibrating_text = 'Calibrating'
        self.exit_calibrate = self.path + 'error_exit_calibrate.png'
        self.home_confrim = self.path + 'SWTST_272_confirm_home.png'
        self.verification_text = 'Flow verification'
        self.troubleshoot = self.path + 'troubleshoot.png'
        self.use_manual_flood = self.path + 'use_manual_flood.png'
        self.verify_viscosity = self.path + 'verify_viscosity.png'
        self.start_manual_flood = self.path + 'start_manual_flood.png'
        self.stop_manual_flood = self.path + 'stop_manual_flood.png'
        self.set_viscosity = self.path + 'set_viscosity.png'
        self.stop = self.path + 'stop.png'
        self.continue_calibrate = self.path + 'continue_calibrate.png'

# class containing the button template paths for formulation
class Formulate:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Formulate\\'
        self.formulation = self.path + 'formulate.png'
        self.start_formulation = self.path + 'start_formulation.png'
        self.okay = self.path + 'ok.png'
        self.complete_batch = self.path + 'complete_batch.png'
        self.confirm_done = self.path + 'confirm_done.png'
        self.done = self.path + 'done.png'
        self.home = self.path + 'home.png'
        self.done_batch = self.path + 'done_batch.png'
        self.next = self.path + 'next.png'
        self.approve_save = self.path + 'approve_save.png'
        self.save = self.path + 'save_unapproved.png'
        self.ok = self.path + 'ok.png'
        self.password = self.path + 'password.png'
        self.no_comment = self.path + 'no_comment.png'
        self.previous = self.path + 'previous.png'

# class containing the button template paths for login
class System_State:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\System_State\\'
        self.logged_out = self.path + 'logged_out.png'
        self.confirm_login = self.path + 'confirm_login.png'
        self.install = self.path + 'install.png'
        self.batch_plan = self.path + 'batch_plan.png'
        self.prime = self.path + 'prime.png'
        self.calibrate = self.path + 'calibrate.png'
        self.formulate = self.path + 'formulate.png'
        self.formulate_complete = self.path + 'formulate_complete.png'
        self.uninstall = self.path + 'uninstall.png'
        

#class containing the buitton template paths for creating new recipe 
class Create_Recipe:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Create_Recipe\\'
        self.recipes = self.path + 'recipes.png'
        self.create_new = self.path + 'create_new.png'
        self.clear_filters = self.path + 'clear_filters.png'
        self.description = self.path + 'description.png'
        self.dilutent = self.path + 'dilutent.png'
        self.done = self.path + 'done.png'
        self.filter = self.path + 'filter.png'
        self.flow = self.path + 'flow.png'
        self.flow_monitoring = self.path + 'flow_monitoring.png'
        self.fluid_path = self.path + 'fluid_path.png'
        self.formulation = self.path + 'formulation.png'
        self.line_a = self.path + 'line_a.png'
        self.line_b = self.path + 'line_b.png'
        self.name = self.path + 'name.png'
        self.next = self.path + 'next.png'
        self.nxgen = self.path + 'nxgen.png'
        self.open_recipe = self.path + 'open_recipe.png'
        self.reagent = self.path + 'reagent.png'
        self.recipes = self.path + 'recipes.png'
        self.start_batch = self.path + 'start_batch.png'
        self.unreleased_off = self.path + 'unreleased_off.png'
        self.unreleased_on = self.path + 'unreleased_on.png'
        self.use_dilution = self.path + 'use_dilution.png'
        self.viscosity = self.path + 'viscosity.png'
        self.volume = self.path + 'volume.png'

class Uninstall:
    def __init__(self):
        self.path = base_path + '\\HMI_Buttons\\Uninstall\\'
        self.uninstall = self.path + 'uninstall.png'
        self.start_uninstall = self.path + 'start_uninstall.png'
        self.run_flush = self.path + 'run_flush.png'
        self.stop_flush = self.path + 'stop_flush.png'
        self.flush_line = self.path + 'flush_line.png'
        self.flush_volume = self.path + 'flush_volume.png'
        self.next = self.path + 'next.png'
        self.disconnect = self.path + 'disconnect.png'
        self.run_drain = self.path + 'run_drain.png'
        self.stop_drain = self.path + 'stop_drain.png'
        self.done = self.path + 'done.png'
        self.removal = self.path + 'removal.png'
        self.done_point = self.path + 'done_point.png'
        self.flushing = self.path + 'flushing.png'
