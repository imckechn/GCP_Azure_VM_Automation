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

awsVMs = []
for i in range(10):
    try:
        ans = buildVMs(azureConfig['azure0' + str(i)])
        awsVMs.append(ans)

    except:
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