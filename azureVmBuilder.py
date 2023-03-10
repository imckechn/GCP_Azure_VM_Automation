# Import the needed credential and management objects from the libraries.
import datetime
import os
import subprocess
from subprocess import PIPE, run

def azureBuildVMs(vmNum, config):
    data = [vmNum]

    try:
        name = config['name']
        resourceGroup = config['resource-group']
        image = config['image']
        # if image == "Debian":
        #     image = 'debian'
        location = config['location']
        adminUsername = config['admin-username']

        data.append(config['purpose'])
        data.append(config['os'])
        data.append(config['team'])

        print("Running 'az group create --name " + resourceGroup + " --location " + location + "' to create a resource group")
        os.system("az group create --name " + resourceGroup + " --location " + location)

        print("Running 'az vm create" +
                        " --resource-group " + resourceGroup +
                        " --name " + name +
                        " --image " + image +
                        " --location " + location +
                        " --admin-username " + adminUsername +
                        " --generate-ssh-keys" +
                        "' to create an Azure VM"
        )
        ans = subprocess.run("az vm create" +
                        " --resource-group " + resourceGroup +
                        " --name " + name +
                        " --image " + image +
                        " --location " + location +
                        " --admin-username " + adminUsername +
                        " --generate-ssh-keys",
                        capture_output=True, shell=True, text=True
        )
        print(ans)

        #Get the time the VM finished being created at
        data.append(datetime.datetime.now())

        return data

    except Exception as e:
        print("Azure VM #", vmNum, " is bad")
        return False
