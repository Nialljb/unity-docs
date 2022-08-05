# Getting setup on Flywheel
v1.0 ~ August 2022  

## Web login
A Google account needs to be linked in order to access the Flywheel platform. (Check with site admin). Once this is done you can access the site by going to our unique URL below and entering your Google credentials.  
(The following links may be useful to save in the bookmark bar of a web browser)

**Login link**
[sent to your email]

**Flywheel documentation**
https://docs.flywheel.io/hc/en-us


When logged into our dedicated site. There will be a list of projects you may have access to in a certain capacity. If there is a project that you cannot see that you believe should be there contact a system admin to grant permissions to that project. 


## Uploading data

### Setup
There are two ways to upload data.
1. via the web console
2. the command line interface (CLI)

The command line interface is the preferred  option, particularly when handling large amounts of data. To do this some dependencies need to be installed on your local machine so it can talk to the Flywheel platform. There are detailed instructions provided here:  
https://docs.flywheel.io/hc/en-us/articles/360008162214-Installing-the-Flywheel-Command-Line-Interface-CLI- 

*Step 1:  Download*  
In the upper-right corner, select your account menu, and select Profile. Here there will be the option to download the CLI for your system. If on a Mac Flywheel will need to be added as a security exception in system preferences. *If on a brand new mac it may be necessary to start in safemode and allow system modifications under security options.    
*Step 2: Generate an API key*  
Also under Flywheel Profile tab (Do not share)  
*Step 3: Navigate to the fw.exe or fw app*  
Move to somewhere it can be run from. Ideally on your system path.  
*Step 4: Log in from the CLI*   
Should be possible to login via the command line with the site adress and your API   
> fw login [url].flywheel.io:[PERSONAL_API_KEY(DO NOT SHARE)]   

<p>&nbsp;</p>

### Sending local data to Flywheel via the CLI
The following is an example of a shell script (send2Flywheel.sh) that will copy data from a project folder on a local machine to flywheel. It will check of data already sent so acts as a good rolling backup.

> \# Flywheel login (add path to profile)  
> fw login [url].flywheel.io:[PERSONAL_API_KEY(DO NOT SHARE)]  
> \# Set path to data  
> sourceDir=~/scratch/DOLPHIN/  
> fw ingest dicom --detect-duplicates ${sourceDir} global_map "UCT (DOLPHIN)"   

- fw = flywheel CLI command
- ingest = command to collect data
- --detect-duplicates will search the flywheel platform for data already ingested
- ${sourceDir} = directory on local machine containing data to send to flywheel
- global_map = name of group where the projects (sites) are stored
- "UCT (DOLPHIN)" = name of specific project data is associated with

If setup as a shell script like above, remember the fw command needs to be set in $PATH otherwise the fullpath will need to be specified. for Mac/Linux
> sudo mv ./fw /usr/local/bin

The shell script will neee permissions to be run(executed):
> chmod +wrx ~/nan/repos/Flywheel/send2Flywheel.sh 

- chmod = change permissions command
- +rwx = flages to add read, write, execute

Now all that is required to update data being sent to Flywheel is to run the script:
> ./send2Flywheel.sh

<p>&nbsp;</p>

The first 20min of the Flywheel webinar provides more information (can be played at X1.25 speed)  
https://www.youtube.com/watch?v=ASf8mDOrFXw&ab_channel=Flywheel.io
