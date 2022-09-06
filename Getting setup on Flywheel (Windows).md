# Getting setup on Flywheel (Windows)
v1.0 ~ August 2022  

## Web login
A Google account needs to be linked in order to access the Flywheel platform. (Check with site admin). Once this is done you can access the site by going to our unique URL below and entering your Google credentials.  
(The following links may be useful to save in the bookmark bar of a web browser)

**Login link**
[sent to your email]

**Flywheel documentation**
https://docs.flywheel.io/hc/en-us


When logged into our dedicated site. There will be a list of projects you may have access to in a certain capacity. If there is a project that you cannot see that you believe should be there contact a system admin to grant permissions to that project. 


**Video walkthrough for getting setup with the command line interface (CLI)**  
https://www.youtube.com/watch?v=01iTpUN_qRM&ab_channel=NiallBourke  

**Video walkthrouhg for uploading data to Flywheel via the CLI**  
https://www.youtube.com/watch?v=pGcbQE5uNog&ab_channel=NiallBourke  


## Uploading data

### Setup
There are two ways to upload data.
1. via the web console
2. the command line interface (CLI)

The command line interface is the preferred  option, particularly when handling large amounts of data. To do this some dependencies need to be installed on your local machine so it can talk to the Flywheel platform. There are detailed instructions provided here:  
https://docs.flywheel.io/hc/en-us/articles/360008162214-Installing-the-Flywheel-Command-Line-Interface-CLI- 

*Step 1:  Download*  
In the upper-right corner, select your account menu, and select Profile. Here there will be the option to download the CLI for your system. 
<img width="1614" alt="Screenshot 2022-08-09 at 17 29 24" src="https://user-images.githubusercontent.com/22872947/183707028-cc3e8d46-39ff-436f-a096-a4f32448e1a5.png">
If on a Mac Flywheel will need to be added as a security exception in system preferences before you can open. *If on a mac pro (M1 max chip) it may be necessary to start in safemode and allow user managment of system terminal extensions under security options.* 

*Step 2: Generate an API key*  
Also under Flywheel Profile tab (Do not share)    

*Step 3: Navigate to the fw.exe or fw app*  
Move to somewhere it can be run from. Ideally on your system path. See Flywheel documentation in link above for more information.



*Step 4: Log in from the CLI*     
Should be possible to login via the command line with the site adress and your API   
From Command Prompt on Windows (open by typing Command Promt in start menu search bar)

> fw login [url].flywheel.io:[PERSONAL_API_KEY(DO NOT SHARE)]     

If successful you will get a notification that you are logged in. To run you need to be in the folder of the fw executable file or have it saved somewhere in your system path.


<p>&nbsp;</p>

### Sending local data to Flywheel via the CLI
This is an example of the folder hierarchy of data as it comes from the Hyperfine scanner (note: acquisition names will vary). The user provides the subject ID at the scanner. This should not contain any special characters and should contain leading 0s. (see for more information: https://github.com/Nialljb/unity-docs/blob/main/UNITY-data-naming-SOP.md)

for exmaple:
- BETA001  
- GAMMA001 
- ECHO001  

not:  

- BETA_1  
- GAMMA-001  
- ECHO(01) 

Example data can be downloaded from here:
https://drive.google.com/file/d/1sgyrTc3dsKm4cGlo-WDDhVz7EbaTxE2g/view?usp=sharing


![image](https://user-images.githubusercontent.com/22872947/184114225-8f1b4b3e-6243-429f-abf6-e146861a74b9.png)

### On the command line
First you need to open terminal and navigate to where the data is stored, then;  
Connect/login to the CLI (command line interface) and finally;    
Run the import command pointing to the folder where the data is  

> Open terminal by typing Command Prompt in the start menu search bar  

![image](https://user-images.githubusercontent.com/22872947/184115604-36c97886-62ad-4459-9ee7-a4e7f7e3d78f.png)

> fw login bmgf.flywheel.io.xxxxxxx = Flywheel login command we have set up. This contains the users unique key at the end which should not be shared. When this is run succesfully it will return a line saying you are logged in.   

> fw ingest dicom --detect-duplicates fw_example dev "example" = This line sends the data inside the folder fw_example to the project example in the group dev on the Flywheel platform. For sending real data dev needs to be replaced by *global_map* and "example" needs to be replaced by *your project name*  

After this command is run some output will be generated in the terminal. A review of the expected folder structure will be provided with the number of subjects and sessions. Have a look at this to check if it is what is expected. If so respond by typing "yes" to the prompt. The data will start uploading to the Flywheel platform.  

The data will be uploaded to the Flywheel platform under the project and group specified(here group = dev, project = example). Opening up the Flywheel web browser we can see the subject and scans that have been uploaded. The subject label and time stamp are given on the left hand side and the list of scans are given on the right. In this example the dicom files from the scanner have automatically been converted to NIFTI the analysing file format. Going forward additional functionality will be added to curate and analyse the data on this platform as new data is added. 
<img width="1634" alt="image" src="https://user-images.githubusercontent.com/22872947/184119424-c5ee23fc-237c-46c6-af92-1534d7225fd8.png">

<p>&nbsp;</p>

The first 20min of the Flywheel webinar provides more information (can be played at X1.25 speed)  
https://www.youtube.com/watch?v=ASf8mDOrFXw&ab_channel=Flywheel.io
