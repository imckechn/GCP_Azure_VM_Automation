import configparser
import datetime
import json
from azureVmBuilder import *
from gcpVmBuilder import *
import os
import subprocess

#CONSTANTS
PROJECT_ID = 'cis4010a3-380020'


# Read the config files
azureConfig = configparser.ConfigParser()
gcpConfig = configparser.ConfigParser()

azureConf = "confFiles/azure.conf"
gcpConf = "confFiles/gcp.conf"
awsExists = False
gcpExists = False

if os.path.isfile(azureConf):
    awsExists = True
    azureConfig.read(azureConf)

if os.path.isfile(gcpConf):
    gcpExists = True
    gcpConfig.read(gcpConf)

# Azure
print("---Creating the Azure VMs---\n")

azureVMs = []
if awsExists:

    #Get the resource grous
    resourceGroups = []
    for i in range(1, 11):
        try:
            if i < 10:
                group = azureConfig['azure0' + str(i)]['resource-group']
            else:
                group = azureConfig['azure' + str(i)]['resource-group']

            if group not in resourceGroups:
                resourceGroups.append(group)
                print("Creating group " + group)
                subprocess.run("az group create --name " + group + " --location canadacentral",capture_output=True, shell=True, text=True)

        except Exception as e:
            break

    #Now create the VMS
    for i in range(1, 10):
        try:
            confData = azureConfig['azure0' + str(i)]
            ans = azureBuildVMs(i, confData)

            if not ans:
                print("Error building VM #", i)
                break
            else:
                azureVMs.append(ans)

        except Exception as e:
            print("Found ", i - 1, " VMs")
            break

    #Now check for a tenth VM since it's naming convention changes
    try:
        ans = azureBuildVMs(azureConfig['azure10'])
        azureVMs.append(ans)
    except:
        pass


# GCP
print("\n\n---Now creating the GCP VMs---\n")

#Set the project id
print("Running'gcloud config set project " + PROJECT_ID + "' to create a GCP project")
subprocess.run("gcloud config set project " + PROJECT_ID, capture_output=True, shell=True, text=True)

gcpVMs = []
if gcpExists:
    #Now create the VMS
    for i in range(1, 11):
        try:
            if i < 10:
                confData = gcpConfig['gcp0' + str(i)]
            else:
                confData = gcpConfig['gcp' + str(i)]

            ans = gcpBuildVMs(i, confData)

            if not ans:
                print("Error building VM #", i)
                break
            else:
                gcpVMs.append(ans)

        except Exception as e:
            print("Found ", i - 1, " VMs")
            break


# Updating the VMcreation file
print("\n\n---Creating/Updating the VMcreation file---\n\n")
time = datetime.datetime.now()
f = open("VMcreations/VMcreation_" + str(time) + ".txt", "w")

f.write("Azure VMs:\n")
f.write("VM #, Purpose, OS, Team\n")
for elem in azureVMs:
    f.write(json.dumps(elem) + "\n")

f.write("GCP VMs:\n")
f.write("VM #, Purpose, OS, Team\n")
for elem in gcpVMs:
    print("elem: ", elem)
    f.write(json.dumps(elem) + "\n")
