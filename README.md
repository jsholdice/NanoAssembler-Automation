# README #

Example code adapted from my work at Preciosn NanoSystems, now a subsidiary of Cytiva, to automate test procedures on the NanoAssembler Commercial Formulation System. Some files have been removed.
NanoAssembler Website: https://www.precisionnanosystems.com/platform-technologies/product-comparison/nanoassemblr-commercial-formulation-system

Python scripts that navigate the HMI remotely either via the HMI website or via the SmartClient app to automate simple procedures.

* The idea of this repo came when running the Frame 1 testing on Enfield.  In general Frame 1 testing is:
	* Testing that is run on the Enfield system by running various recipes.
	* A jig with extra sensors (Not in Enfield BOM) is attached to the Enfield and used for logging.
	* Data is captured during a set of recipe formulations and recorded via the jig.
	* Scripts analyse the data and determine if the Enfield requirements are being met.
* When doing a frame 1 test you end up running many recipes meaning the same set up button clicks over and over.
* This code is intended to automate that, so the tester does not need to stand in front of the enfield all day when running the tests.
* The code acts on an active window that is showing the HMI screens.  (It does not act on the HMI screen directly)
	* The window to show the HMI screen is done through a tool from Siemens called the SmartClient.

### What does the repository contain? ###

* Procedures include running recipes through to formulation and simple troubleshooting capabilities along the way. 
* Additionally, the retieve_batch_record.py script will download a large number of batch records off the HMI SD card 

### How to use the Repo ###

* Installation Procedure 
	* Naviage to the enfield_hmi_remote_control repository on Bitbucket
	* Clone the repo and copy https to clipboard
		* Create directory on local computer where you want the repo to reside
		* Open powershell in directory and paste to the comand line (git clone https:...)
	* Once repo is created, navigate to enfield_hmi_remote_control (cd enfield_hmi_remote_control)
	* Type 'pip install -r requirements.txt' into command line to import neccessary modules
	* Confirm you are using Python 3.11 (type in cmd line: 'python --version')
	* Ensure ThinkPad laptop is set as the primary display in Settings -> Systems -> Display -> Make this my main display
	* Type 'python recipe_run.py' into command line to run first start up sequence, which will automatically:
		* Establish VNC connection with the Enfield 
		* Scale remote HMI screen to fit appropriately on user's screen
		* Resize HMI_Image_Library png to match new user's screen size
