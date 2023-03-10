import configparser
from azureVmBuilder import *
from gcpVmBuilder import *

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
print("---Now runing Azure---\n\n")

# azureVMs = []
# if awsExists:
#     #Get the resource grous
#     # print("Running 'az group create --name images --location canadacentral' to create a resource group on Azure")
#     # os.system("az group create --name images --location canadacentral")

#     resourceGroups = []
#     for i in range(1, 11):
#         try:
#             if i < 10:
#                 group = azureConfig['azure0' + str(i)]['resource-group']
#             else:
#                 group = azureConfig['azure' + str(i)]['resource-group']

#             if group not in resourceGroups:
#                 resourceGroups.append(group)
#                 os.system("az group create --name " + group + " --location canadacentral")

#         except Exception as e:
#             break

#     #Now create the VMS
#     for i in range(1, 10):
#         try:
#             confData = azureConfig['azure0' + str(i)]
#             ans = azureBuildVMs(i, confData)

#             if not ans:
#                 print("Error building VM #", i)
#                 break
#             else:
#                 azureVMs.append(ans)

#         except Exception as e:
#             print("Found ", i - 1, " VMs")
#             break

#     #Now check for a tenth VM since it's naming convention changes
#     try:
#         ans = azureBuildVMs(azureConfig['azure10'])
#         azureVMs.append(ans)
#     except:
#         pass

# print("Azure VMs: ", azureVMs)

# GCP
print("\n\n---Now runing GCP---\n\n")

#Set the project id
print("Running'gcloud config set project " + PROJECT_ID + "' to create a GCP project")
os.system("gcloud config set project " + PROJECT_ID)

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

print("GCP VMs: ", gcpVMs)