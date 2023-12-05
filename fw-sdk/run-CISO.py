import flywheel
import os
import pandas as pd
from pathlib import Path
import pathvalidate as pv
from datetime import datetime

"""
Python script to run the CISO gear on all subjects in a project
1. Connect to Flywheel API
2. Define the project and gear
3. Create a local work directory to store the results/logs
4. Iterate through all subjects in the project and find the T2 acquisitions
5. Find the target template based on the age at scan
6. Submit the job
7. Save the report to a csv file

Dependencies:
- flywheel-sdk
- pathvalidate
- pandas

The script is designed to be run from the command line.
Requires the Flywheel CLI & Flywheel SDK to be installed 

Usage:
- Set the environment variable FW_CLI_API_KEY to your Flywheel API key
- Set the group_name and project_name variables to the project you want to run the gear on
- Set the gear_name variable to the gear you want to run
- Run the script

"""

# --- Set up the Flywheel CLI and SDK ---

# Flywheel API Key
api_key = os.environ.get('FW_CLI_API_KEY') # Set your API key as an environment variable
fw = flywheel.Client(api_key=api_key)

group_name = "global_map" # Default for all UNITY projects
project_name = "UCT-Khula-Hyperfine" # Change this to the project you want to run the gear on
project = fw.lookup(f"{group_name}/{project_name}")
ciso_gear =  fw.lookup('gears/ciso')

# Initialize gear_job_list
job_list = list()
inputs = {} 

# Initialize a dictionary for easy csv export
report = {'subject':[]}

# Create a working directory in our local "home" directory
work_dir = Path(Path.home()/'GD/work/Kings/analysis/fw-derivatives/', platform='auto')
# If it doesn't exist, create it
if not work_dir.exists():
    work_dir.mkdir(parents = True)
# Create a custom path for our project (we may run this on other projects in the future) and create if it doesn't exist
project_path = pv.sanitize_filepath(work_dir/project.label, platform='auto')
if not project_path.exists():
    project_path.mkdir()


# --- Iterate through all subjects in the project and find the T2 acquisitions ---

# Iterate through all subjects in the project and find the T2 acquisitions
for subject in project.subjects.iter():
    for session in subject.sessions.iter():
        session = session.reload()
        print("parsing... ", subject.label, session.label)

        # Look at every acquisition in the session
        for acq in session.acquisitions.iter():
            acq = acq.reload()
            for file_obj in acq.files:
                # We only want anatomical Nifti's              
                if file_obj.type == 'nifti' and 'T2' in file_obj.name and 'AXI' in file_obj.name:           
                    input_label = 'axi'
                    inputs[input_label] = file_obj
                if file_obj.type == 'nifti' and 'T2' in file_obj.name and 'COR' in file_obj.name:           
                    input_label = 'cor'
                    inputs[input_label] = file_obj
                if file_obj.type == 'nifti' and 'T2' in file_obj.name and 'SAG' in file_obj.name:           
                    input_label = 'sag'
                    inputs[input_label] = file_obj

                # Get DOB from dicom header and calculate age at scan to determine target template
                if file_obj.type == 'dicom' and 'T2' in file_obj.name and 'AXI' in file_obj.name:

                    # Get DOB from dicom header
                    try:
                        dob = file_obj.info['PatientBirthDate']
                    except:
                        print("No DOB in dicom header")
                        print("Adding to missing report...")
                        report['subject'].append(subject.label)
                        continue
                    
                    # print("dob: ", dob)
                
                    # Get series date from dicom header
                    seriesDate = file_obj.info['SeriesDate']
                    # print("seriesDate: ", seriesDate)
                    
                    # Calculate age at scan
                    age = (datetime.strptime(seriesDate, '%Y%m%d')) - (datetime.strptime(dob, '%Y%m%d'))
                    # Find the target template based on the session label
                    age = age.days
                    print("age: ", age)

                    # Make sure age is positive
                    if age < 0:
                        age = age * -1

                    # Find the target template based on the age at scan
                    if age < 15:
                        target_template = 'BCP-00M-T2.nii'
                    if age < 45:
                        target_template = 'BCP-01M-T2.nii'
                    elif age < 75:
                        target_template = 'BCP-02M-T2.nii'
                    elif age < 105:
                        target_template = 'BCP-03M-T2.nii' 
                    elif age < 200:
                        target_template = 'BCP-06M-T2.nii' 
                    elif age < 400:
                        target_template = 'BCP-12M-T2.nii'
                    elif age < 600:
                        target_template = 'BCP-18M-T2.nii'
                    elif age < 900:
                        target_template = 'BCP-24M-T2.nii'
                    elif age < 1320:
                        target_template = 'nihpd_asym_33-44_t2w.nii'
                    elif age < 2000:
                        target_template = 'nihpd_asym_44-60_t2w.nii'
                    else:
                        target_template = 'MNI152_T1_1mm.nii'
                        print("Older than 2000 days (5.5 years), using MNI152_T1_1mm.nii")

                    print("target_template: ", target_template)

# --- Submit the job ---

        try:
            # The destination for this anlysis will be on the session
            dest = session
            time_fmt = '%d-%m-%Y_%H-%M-%S'
            analysis_label = f'ciso{datetime.now().strftime(time_fmt)}' 
            job_id = ciso_gear.run(analysis_label=analysis_label, inputs=inputs, destination=dest, tags=['sdk'], config={
            "target_template": target_template,
            "verbose": "v"
        })
            job_list.append(job_id)
            print("Submitting Job: Check Jobs Log", dest.label)
        except:
            print("BOOP: Job cannot be sent.. No files for session??", dest.label)

# --- Save the report to a csv file ---

# Now save the report to a csv file using pandas, the easiest way to save this kind of data
# In the format that we want.
csv_file = os.path.join(project_path, f"{project.label}_missing_DOB.csv")
df = pd.DataFrame(report)
df.to_csv(csv_file, index=False)
