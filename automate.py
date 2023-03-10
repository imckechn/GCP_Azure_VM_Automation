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
azureExists = False
gcpExists = False

if os.path.isfile(azureConf):
    azureExists = True
    azureConfig.read(azureConf)

if os.path.isfile(gcpConf):
    gcpExists = True
    gcpConfig.read(gcpConf)

# Azure
print("---Creating the Azure VMs---\n")

azureVMs = []
if azureExists:

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
    for i in range(1, 11):
        try:
            if i < 10:
                confData = azureConfig['azure0' + str(i)]
                ans = azureBuildVMs(i, confData)
            else:
                confData = azureConfig['azure' + str(i)]
                ans = azureBuildVMs(i, confData)

            if ans == False:
                print("Error building VM #", i)
                break
            elif ans != None:
                azureVMs.append(ans)

        except Exception as e:
            print("Found ", i - 1, " Azure VMs")
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

            if ans == False:
                print("Error building VM #", i)
                break

            elif ans != None:
                gcpVMs.append(ans)

        except Exception as e:
            print("Found ", i - 1, " GCP VMs")
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
    f.write(json.dumps(elem) + "\n")


#Rename the .conf files
if azureExists:
    os.rename('confFiles/azure.conf', 'confFiles/azure' + str(datetime.datetime.now()) + '.conf')
if gcpExists:
    os.rename('confFiles/gcp.conf', 'confFiles/gcp' + str(datetime.datetime.now()) + '.conf')

#Open the ports for Azure
while True:
    ans = input("Do you want to open any ports for Azure(y/n)? ")
    if ans == 'y':
        azureOpenPorts()
        break
    elif ans == 'n':
        break
    else:
        print("Please enter 'y' or 'n'")

#open the ports for GCP
while True:
    ans = input("Do you want to open any ports for GCP(y/n)? ")
    if ans == 'y':
        gcpOpenPorts()
        break
    elif ans == 'n':
        break
    else:
        print("Please enter 'y' or 'n'")
