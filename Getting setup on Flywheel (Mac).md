# Getting setup on Flywheel (Mac)
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
https://youtu.be/NcM6oTUz8O8

**Video walkthrouhg for uploading data to Flywheel via the CLI**   
https://www.youtube.com/watch?v=X7u_0cjG72U&ab_channel=NiallBourke 


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

From terminal on Mac (open by pressing command + space and start typing Terminal)
> sudo cp ~/Downloads/darwin_amd64/fw /usr/local/bin/

*Step 4: Log in from the CLI*     
Should be possible to login via the command line with the site adress and your API     
> fw login [url].flywheel.io:[PERSONAL_API_KEY(DO NOT SHARE)]     

<p>&nbsp;</p>

### Sending local data to Flywheel via the CLI
This is an example of the folder hierarchy of data as it comes from the Hyperfine scanner (note: acquisition names will vary). The user provides the subject ID at the scanner. This should not contain any special characters and should contain leading 0s. 

for exmaple:
- BETA001  
- GAMMA001 
- ECHO001  

not:  

- BETA_1  
- GAMMA-001  
- ECHO(01) 

Example data can be downloaded from here:
https://drive.google.com/drive/folders/13trxqRo2PNEk-JuwUKH2kEL9pSWwo8w-?usp=sharing


<img width="1356" alt="image" src="https://user-images.githubusercontent.com/22872947/184101565-8feb13fe-0990-4fe8-b357-89f219e03630.png">


### On the command line
First you need to open terminal and navigate to where the data is stored, then;  
Connect/login to the CLI (command line interface) and finally;    
Run the import command pointing to the folder where the data is  

> Open terminal by pressing command + spacebar  
> Start typing: Terminal  

<img width="795" alt="Screenshot 2022-08-11 at 10 42 17" src="https://user-images.githubusercontent.com/22872947/184106904-70eb323f-b6af-4546-b03a-74c0066711af.png">

> pwd = print working directory. Shows where on the computer path you are located  

> ls = list contents of current directory. Here we are in Downloads and there is one folder "fw_example"  

> fw login bmgf.flywheel.io.xxxxxxx = Flywheel login command we have set up. This contains the users unique key at the end which should not be shared. When this is run succesfully it will return a line saying you are logged in.   

> fw ingest dicom --detect-duplicates fw_example dev "example" = This line sends the data inside the folder fw_example to the project example in the group dev on the Flywheel platform. For sending real data dev needs to be replaced by *global_map* and "example" needs to be replaced by *your project name*  

After this command is run some output will be generated in the terminal. A review of the expected folder structure will be provided with the number of subjects and sessions. Have a look at this to check if it is what is expected. If so respond by typing "yes" to the prompt. The data will start uploading to the Flywheel platform.  

The data will be uploaded to the Flywheel platform under the project and group specified(here group = dev, project = example). Opening up the Flywheel web browser we can see the subject and scans that have been uploaded. The subject label and time stamp are given on the left hand side and the list of scans are given on the right. In this example the dicom files from the scanner have automatically been converted to NIFTI the analysing file format. Going forward additional functionality will be added to curate and analyse the data on this platform as new data is added.  

<img width="1634" alt="image" src="https://user-images.githubusercontent.com/22872947/184119528-a0c15bb0-790c-4551-baed-fa9e54adf66f.png">

<p>&nbsp;</p>

**Project sepecific data upload requirements**
For specfic projects data may be organised or labeled in such a way we need to create a template to read the data and upload it. Once the CLI credentials have been setup we can make this template file and unique command to run in order to upload data. Please speak to me about this if required.  

The first 20min of the Flywheel webinar provides more information   
https://www.youtube.com/watch?v=ASf8mDOrFXw&ab_channel=Flywheel.io

## Mac troubleshooting Flywheel setup

### Mac silicon chip security settings
On the latest Macs with silicon chips it may be necessary to change the startup disk security settings to allow use of kernal extensions. To do so follow the instructions below. During the process an adminstrators details may be required. 

1. Shut down the computer
2. Press and hold the power button. Keep holding and a message should appear "Loading startup options"
3. Select "Options"   
![IMG_3373](https://user-images.githubusercontent.com/22872947/187472357-a6da995b-9745-4b76-ab18-0d62fbb59026.JPG)

4. When the menu appears, ignore this. Select the Utilities > Startup Security Utility from the toolbar menu on the top left of the screen  
![IMG_3375](https://user-images.githubusercontent.com/22872947/187472496-a976ca0d-8da4-438a-8d2b-b0aa6dc33c2c.JPG)

5. Select the startup disk  
![IMG_3376](https://user-images.githubusercontent.com/22872947/187472595-abd4b201-7863-4af3-bd8b-70fab1a9cae9.JPG)

6. Select "Reduced Security" & "Allow user management of kernal extensions from identified developers" 
![IMG_3377](https://user-images.githubusercontent.com/22872947/187472793-3f0662db-e434-44fb-895e-879c695e0543.JPG)

7. Click "OK"
8. When the changes are applied restart the computer and continue with installation. 


In some instances it may be necessary to install Rosetta on Macs with the new silicon chip if it is not already available. This simply improves compatability with software designed with intel chips. 

1. Open Terminal (Command + space), type Terminal
2. copy and paste the following:
    > softwareupdate --install-rosetta

For more information:
https://support.apple.com/en-us/HT211861

