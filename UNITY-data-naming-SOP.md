# UNITY data labelling
V1.0 July 2022   

---
## Overview
    
An important motivation of the consortium is to standardise and automate analysis. To this end some standard conventions should be used. When collecting and organising data if a standardised structure is implemented, the following analysis steps can run efficiently. Through FlyWheel we will arrange data in the BIDS (Brain Imaging Data Structure) format https://bids.neuroimaging.io/  

Organisation of data into the BIDS format will be implemented through FlyWheel. However, there are steps that can be taken when labelling participants on the scanner that will make adding each new site less work.
To make this a smooth process some **best practice** guidelines will be provided. *The automation of data processing is largely dependent on consistency and standardisation of user input.* Each project may have their own specific requirements, which can be adapted to. Where possible it is preferred to stick as closely to the REPROIN convention at the scanner.   

https://dbic-handbook.readthedocs.io/en/latest/mri/reproin.html  

However, this may not be possible, as we cannot currently changes Hyperfine acquisition labels but we do have control over the participant naming. 

    The key is to be consistent

- scan aquisition names = defined by Hyperfine
- scan session labels = user input 
- demographic spreadsheets = user input

### Hyperfine MRI data collection
To get an idea of best naming practice when collecting data on the scanner please see an example for the UNITY consortium final folder & file strucrure:

**folder hierarchy:** 
> /project/subject/session/modality/acquisition/files

For example:
> /BETA/sub-BETA001/ses-visit001/anat/T1w/BETA001_ses-visit001_aqc-T1w.nii.gz

**file structure:**
> sub-[ID]_ses-[number]_aqc-[scan type]

An example of the final file would look like this:
> sub-test001_ses-visit01_aqc-T1w.nii.gz
 
You can see here all characters are lowercase and each important bit of information is consistently prefixed with an identifier ( - ) and separated by and underscore ( _ ). It is ok to have CAPS in subject IDs but this should be consistent across all subjects for a project.
 With this structure applied to all data it becomes easy to __parse__ the relevant information relating to subject, scanning session, modality and to automate analysis pipelines. 

## Labelling on the scanner 
### (assigning participant IDs)

It is important to note that how a file is named can greatly impact how easy it is to parse (organise) data programmatically. What sometimes looks like it makes sense in human readable format can cause issues for the machine. 

Computers handle spaces as separate bits of information.  
"participant 01" would be read as 
- participant 
- 01    

In this case for a single item of information no space should be included. If you want to pair one bit of information (subject ID) with something else say the session visit this should be done with an underscore (_)
- participant001_visit01

Notice how I use zero padding before the number 001 rather than 1. This is because without it when organising the data in alphanumeric order participant1 would be put next to participant11 and participant111. The zero padding keeps files in the order we would expect them to be. 


Dash (-) and underscore characters (_) are often used as delimiters when programming (separating bits of information). In this case it can be useful to separate the study, participant ID, and the scanning session/visit. It is important to be *consistent* with the use of dashes and underscores. 
For the most part if labelling data, underscores will be preferred as dashes are used in BIDS later on to label the type of information.

A simple structure like the following would be good:
> projectname[ID number]_visit[number]   

For example:   
> BETA001_visit01

Other information should be stored in a demographic database with a subject identifier that matches **exactly** the label that was entered onto the scanner. Typos, case-sensitivity, inconsistent dashes and underscores can cause problems.

**Important:** There are special characters that can make it difficult to handle data such as () or ^ along with blank/white spaces. Here is a list of invalid characters that will result in blocked uploads to Flywheel if they are included in a filename:
> \~  
> \:  
> \*  
> \?  
> “  
> \<  
> \>  
> \|  
> \\  
> Tab  
> Line feed  
> Carriage Return  
> Vertical Tab  
> Form feed   


