# Import the needed credential and management objects from the libraries.
import os

def azureBuildVMs(vmNum, config):
    data = [vmNum]

    try:
        name = config['name']
        resourceGroup = config['resource-group']
        image = config['image']
        if image == "Debian":
            image = 'debian'
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
        ans = os.system("az vm create" +
                        " --resource-group " + resourceGroup +
                        " --name " + name +
                        " --image " + image +
                        " --location " + location +
                        " --admin-username " + adminUsername +
                        " --generate-ssh-keys"
        )

        return data

    except Exception as e:
        print("Azure VM #", vmNum, " is bad")
        return False
