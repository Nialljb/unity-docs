import os
import flywheel
from pathlib import Path
import pathvalidate as pv
import pandas as pd

"""   
Python script to pull SynthSeg summary reports from Flywheel
niall.bourke@kcl.ac.uk June 2023

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

# Setup Flywheel connector
api_key = os.environ.get('FW_CLI_API_KEY') # API key is stored as an environment variable
fw = flywheel.Client(api_key=api_key)

# Set project info
group_name = "consortium" 
project_name = "BETA"
project = fw.lookup(f"{group_name}/{project_name}")
gear='synthSeg'

# preallocate lists
df = []
sub = []
ses = []

# Create a work directory in our local "home" directory
work_dir = Path(Path.home()/'GD/work/Kings/analysis/fw-derivatives/', platform='auto')

# If it doesn't exist, create it
if not work_dir.exists():
    work_dir.mkdir(parents = True)

# Create a custom path for our project (we may run this on other projects in the future) and create if it doesn't exist
project_path = pv.sanitize_filepath(work_dir/project.label/gear, platform='auto')
if not project_path.exists():
    project_path.mkdir(parents = True)

for subject in project.subjects.iter():
    subject = subject.reload()
    sub_label = subject.label
    for session in subject.sessions.iter():
        session = session.reload()
        ses_label = session.label

        print(sub_label, ses_label)
        for analysis in session.analyses:
            # print(analysis.label)
            if "SynthSeg" in analysis.label and analysis.get("job").get("state") == "complete":  # SynthSeg synthseg
                for analysis_file in analysis.files:
                    if "vol.csv" in analysis_file.name:
                        file = analysis_file
                        file = file.reload()
                        print(sub_label, file.name)

                        # Sanitize our filename and parent path
                        download_dir = pv.sanitize_filepath(project_path/sub_label/ses_label,platform='auto')
                        
                        # Create the path
                        if not download_dir.exists():
                            download_dir.mkdir(parents=True)
                        download_path = download_dir/file.name
                        
                        # Download the file
                        print('downloading file', ses_label, file.name)
                        file.download(download_path)
        
                        sub.append(sub_label)
                        ses.append(ses_label)

                        with open(download_path) as csv_file:
                            results = pd.read_csv(csv_file, index_col=None, header=0) 
                            df.append(results)

# write DataFrame to an excel sheet 
df = pd.concat(df, axis=0, ignore_index=True)
outdir = os.path.join(project_path, 'highfield_synthseg_vol.csv')
df.to_csv(outdir)

# write demo to an excel sheet 
dict = {'subject': sub, 'session': ses}  
demo = pd.DataFrame(dict)
demoOutdir = os.path.join(project_path, 'demo.csv')
demo.to_csv(demoOutdir)