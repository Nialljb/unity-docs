import os
import flywheel
import pandas as pd

"""   
Pulls data from mriqc gear output and creates a csv report of SNR values

This script will pull SNR values from the mriqc gear output and create a csv report
of SNR values for each subject/session/acquisition.  It will also flag any data that
does not meet QC standards. Addapted from Flywheel's SDK example script.
https://flywheel-io.gitlab.io/product/backend/sdk/branches/master/python/index.html

Usage:
1. Setup Flywheel CLI and login locally
2. Install flywheel-sdk: pip install flywheel-sdk
3. Set the group_name and project_name variables below
4. Run the script: python mriqc_flywheel.py


"""

# Setup connection to flywheel client
api_key = os.environ.get('FW_CLI_API_KEY')
fw = flywheel.Client(api_key=api_key)

# Define the project we're working in
group_name = "consortium" # This is the group name in flywheel
project_name = "BETA" # This is the project name in flywheel
project = fw.lookup(f"{group_name}/{project_name}")

# Create a data dictionary that will contain key/value pairs.
# This data dict will eventually become a pandas dataframe.
qc_info = {
           'subject':[],
           'session':[],
           'acquisition':[],
           'file':[],
           'snr':[],
           'type':[]
           }

# Iterate through the sessions
for session in project.sessions.iter():

    # Iterate through the acquisitions
    for acq in session.acquisitions.iter():
        acq = acq.reload()

        # Find any files that have the string "mriqc.qa" in them, indicating
        # That it's an output report from the mriqc gear.
        qc_files = [file for file in acq.files if 'mriqc.qa' in file.name]

        # In case there are two qc files in an acquisition, only use one.
        # This can be handled differently depending on the project, but in this example
        # There should only be one qc file per acquisition.
        if len(qc_files) > 1:
            qc_files = [qc_files[0]]

        for qc_file in qc_files:
            # Get the subject, session, and acquisition label, as well as the qc filename
            sub_label = session.subject.label
            ses_label = session.label
            acq_label = acq.label
            fname = qc_file.name

            print(qc_file.classification.get('Measurement'))

            if 'T2' in qc_file.classification.get('Measurement'):
                qc_info['subject'].append(sub_label)
                qc_info['session'].append(ses_label)
                qc_info['acquisition'].append(acq_label)
                qc_info['file'].append(fname)
                qc_info['type'].append('T2')

                snr = qc_file.info.get('snr')
                qc_info['snr'].append(snr)

                # Flag bad data with an appropriate tag if it doesn't meet QC standards:
                if snr < 6.0:
                    acq.add_tag('LOW_SNR')

            # If it's a T1, get the 'snr_total' value (SNR across all brain tissue types)
            # And since there's no FD, simply put "NA".
            # Remember that we need to append one value to each key in our dict to keep the
            # Length of each array the same.  Otherwise, our subject/session/acquisition labels
            # Will get out of sync with our FD data, and the dataframe will be useless.
            elif 'T1' in qc_file.classification.get('Measurement'):
                qc_info['subject'].append(sub_label)
                qc_info['session'].append(ses_label)
                qc_info['acquisition'].append(acq_label)
                qc_info['file'].append(fname)
                qc_info['type'].append('T1')

                snr = qc_file.info.get('snr_total')

                qc_info['snr'].append(snr)

                if snr < 6.0:
                    acq.add_tag('LOW_SNR')

# Create a dataframe from our data dictionary
df = pd.DataFrame.from_dict(qc_info)

# Save the df as a csv output:
csv_out = 'qc_report.csv'
df.to_csv(csv_out,index=False)