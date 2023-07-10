import flywheel
import os
from datetime import datetime

"""
Python script to run the FreeSurfer gear on all subjects in a project
niall.bourke@kcl.ac.uk, June 2023

This script will submit a FreeSurfer job for every T1w anatomical in the project
and is is run from local machine

Usage:
1. Setup Flywheel CLI and login locally
2. Install flywheel-sdk: pip install flywheel-sdk
3. Set the group_name and project_name variables below
4. Adjust the file_ojb.name if statement to match the anatomical you want to run FreeSurfer on
5. Run the script: python run-FreeSurfer.py

*NOTE: A FREESURFER LICENSE MUST BE ADDED TO THE CONFIG OF THE GEAR BEFORE RUNNING THIS SCRIPT*

"""


# Setup connection to flywheel client
api_key = os.environ.get('FW_CLI_API_KEY')
fw = flywheel.Client(api_key=api_key)

# Define the project we're working in
group_name = "consortium"
project_name = "BETA"
project = fw.lookup(f"{group_name}/{project_name}")
reconall_gear =  fw.lookup('gears/freesurfer-recon-all')

input_order = ['anatomical','t1w_anatomical_2','t1w_anatomical_3','t1w_anatomical_4','t1w_anatomical_5']

# Initialize gear_job_list
job_list = list()

# Because this is anatomicals PER subject, we'll collect T1's and T2's over subjects:
for subject in project.subjects.iter():

    # Initialize some values
    current_anat = 0
    have_T2 = False
    full_T1 = False
    inputs = {}

    # The only way to get to acquisitions is to go through the sessions
    for session in subject.sessions.iter():
        print("parsing... ", subject.label, session.label)
        for acq in session.acquisitions.iter():
            if 'MPR_vNav_RMS' in acq.label:
                acq = acq.reload()
                print("analyses: ", acq.analyses)

                if acq.analyses != []:
                    print("Analyses for this acquisition: ", acq.label)
                    for analysis in acq.analyses:
                        print("analysis: ", analysis.label, " & state: ", analysis.get("job").get("state"))
                        # Only proceed if there is not already a completed freesurfer job
                        if "freesurfer" in analysis.label and analysis.get("job").get("state") != "complete":
                            # Now we have to look at every file in every acquisition
                            for file_obj in acq.files:
                                # Exclude this setter nonsense
                                if 'setter' in file_obj.name or 'vNav_e' in file_obj.name:
                                    continue
                                
                                print(file_obj.name)
                                # We only want anatomical Nifti's              
                                if file_obj.type == 'nifti' and file_obj.classification.get('Intent') == ['Structural']: # edit cause orig broke if Intent was empty
                                    print("file name is: ", file_obj.name, "file type is: ", file_obj.type, " & Intent is: ", file_obj.classification.get('Intent'))
                                            
                                    # If we don't already have all our T1's, add this if it's a T1
                                    if not full_T1 and file_obj.classification.get('Measurement') == ['T1'] and 'MPR_vNav_RMS' in file_obj.name:  # 'HBS_MEMPRAGE_nav_RMS' in file_obj.name or
                                        input_label = input_order[current_anat]
                                        inputs[input_label] = file_obj
                                        current_anat += 1
                                        print("t1w input: ", inputs[input_label].name)
                                        # If our current anat input is number 4, we're full
                                        if current_anat > 4:
                                            full_T1 = True

                elif acq.analyses == []:
                    print("No analyses for this acquisition: ", acq.label)
                    for file_obj in acq.files:
                        # Exclude this setter nonsense
                        if 'setter' in file_obj.name or 'vNav_e' in file_obj.name:
                            continue
                        
                        print(file_obj.name)
                        # We only want anatomical Nifti's              
                        if file_obj.type == 'nifti' and file_obj.classification.get('Intent') == ['Structural']: # edit cause orig broke if Intent was empty
                            print("file name is: ", file_obj.name, "file type is: ", file_obj.type, " & Intent is: ", file_obj.classification.get('Intent'))
                                    
                            # If we don't already have all our T1's, add this if it's a T1
                            if not full_T1 and file_obj.classification.get('Measurement') == ['T1'] and 'MPR_vNav_RMS' in file_obj.name:  # 'HBS_MEMPRAGE_nav_RMS' in file_obj.name or
                                input_label = input_order[current_anat]
                                inputs[input_label] = file_obj
                                current_anat += 1
                                print("t1w input: ", inputs[input_label].name)
                                # If our current anat input is number 4, we're full
                                if current_anat > 4:
                                    full_T1 = True


                try:
                    # The destination for this anlysis will be on the session
                    dest = session # subject
                    time_fmt = '%d-%m-%Y_%H-%M-%S'
                    analysis_label = f'Freesurfer_Recon_all_{datetime.now().strftime(time_fmt)}'
                    job_id = reconall_gear.run(analysis_label=analysis_label, inputs=inputs, destination=dest,config={'gear-FREESURFER_LICENSE':'!!!INSERT FREESURFER LICENSE HERE!!!'})
                    job_list.append(job_id)
                    print("Submitting Job: Check Jobs Log", dest.label)
                    # print("Input: ", inputs[input_label].name)
                    print("Input: ", subject.label, session.label, inputs[input_label].name)
                except:
                    print("BOOP: Job cannot be sent.. No files for session??", dest.label, session.label)


