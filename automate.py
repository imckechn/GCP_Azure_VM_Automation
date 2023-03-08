import configparser
from azureVmBuilder import *

# Read the config files
azureConfig = configparser.ConfigParser()
gcpConfig = configparser.ConfigParser()

azureConf = "confFiles/azure.conf"
gcpConf = "confFiles/gcp.conf"

azureConfig.read(azureConf)
gcpConfig.read(gcpConf)

#aws_access_key_id = config['default']['aws_access_key_id']

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
        ans = buildVMs(i, confData)

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
    ans = buildVMs(azureConfig['azure10'])
    awsVMs.append(ans)
except:
    pass

# GCP

# Azure
# azureVMs = []
# azureVMs.append(azureConfig['azure01'])
# azureVMs.append(azureConfig['azure02'])