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
    #awsExists = True
    azureConfig.read(azureConf)

if os.path.isfile(gcpConf):
    gcpExists = True
    gcpConfig.read(gcpConf)

#aws_access_key_id = config['default']['aws_access_key_id']

if awsExists:
    #Get the resource grous
    os.system("az group create --name images --location canadacentral")

    resourceGroups = []
    for i in range(1, 10):
        try:
            group = azureConfig['azure0' + str(i)]['resource-group']

            if group not in resourceGroups:
                resourceGroups.append(group)
                os.system("az group create --name " + group + " --location canadacentral")

        except Exception as e:
            break

    #Now check for a tenth VM since it's naming convention changes
    try:
        group = azureConfig['azure0' + str(i)]['resource-group']

        if group not in resourceGroups:
            resourceGroups.append(group)
            os.system("az group create --name " + group + " --location canadacentral")
    except:
        pass


    #Now create the VMS
    awsVMs = []
    for i in range(1, 10):
        try:
            confData = azureConfig['azure0' + str(i)]
            ans = azureBuildVMs(i, confData)

            if not ans:
                print("Error building VM #", i)
                break
            else:
                awsVMs.append(ans)

        except Exception as e:
            print("Found ", i - 1, " VMs")
            break

    #Now check for a tenth VM since it's naming convention changes
    try:
        ans = azureBuildVMs(azureConfig['azure10'])
        awsVMs.append(ans)
    except:
        pass

# GCP

#Set the project id
os.system("gcloud config set project " + PROJECT_ID)

if gcpExists:
    #Now create the VMS
    gcpVMs = []
    for i in range(1, 10):
        try:
            confData = gcpConfig['gcp0' + str(i)]
            ans = gcpBuildVMs(i, confData)

            if not ans:
                print("Error building VM #", i)
                break
            else:
                gcpVMs.append(ans)

        except Exception as e:
            print("Found ", i - 1, " VMs")
            break

    #Now check for a tenth VM since it's naming convention changes
    try:
        ans = gcpBuildVMs(azureConfig['azure10'])
        gcpVMs.append(ans)
    except:
        pass




# Azure
# azureVMs = []
# azureVMs.append(azureConfig['azure01'])
# azureVMs.append(azureConfig['azure02'])