# GCP_Azure_VM_Automation
### Written By Ian McKechnie
### Date: March 10, 2023

## Description
This program automates the creation of VMs for Azure and Google Cloud. It reads in VM details from conf files in the *confFiles* directory and creates the VMs if they don't already exist. It will then allow you to set the port number for the VMs. It will create a description of the VMs in the *VMcreations* folder.

## How to run
1. Clone the repo
2. ``cd GCP_Azure_VM_Automation``

3. Download the Google Cloud SDK and Azure CLI

- Azure: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Google Cloud: https://cloud.google.com/sdk/docs/install

4. ``gcloud auth login``
5. ``az login``
5. ``pip3 automate.py``

## Repo Structure
Directory confFiles contains the gcp and azure conf files.

VMcreations creates the text output of the VMs created.

Automate.py runs the main program
azureVmBuilder.py creates the VMs for Azure
gcpVmBuilder.py creates the VMs for Google Cloud