import configparser
import azure


# Read the config files
azureConfig = configparser.ConfigParser()
gcpConfig = configparser.ConfigParser()

azureConf = "azure.conf"
gcpConf = "gcp.conf"

azureConfig.read(azureConf)
gcpConfig.read(gcpConf)

#aws_access_key_id = config['default']['aws_access_key_id']


# Azure
azureVMs = []
azureVMs.append(azureConf['azure01'])
azureVMs.append(azureConf['azure02'])