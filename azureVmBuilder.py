# Import the needed credential and management objects from the libraries.
import datetime
∂import subprocess

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


        print("Running 'az vm create" +
                        " --resource-group " + resourceGroup +
                        " --name " + name +
                        " --image " + image +
                        " --location " + location +
                        " --admin-username " + adminUsername +
                        "' to create an Azure VM"
        )
        ans = subprocess.run("az vm create" +
                        " --resource-group " + resourceGroup +
                        " --name " + name +
                        " --image " + image +
                        " --location " + location +
                        " --admin-username " + adminUsername,
                        capture_output=True, shell=True, text=True
        )

        if 'stderr="ERROR' in str(ans):
            print("Azure VM #", vmNum, " is bad")
            return False
        else:
            print("Created Azure VM #", vmNum)

        #Get the time the VM finished being created at
        data.append(str(datetime.datetime.now()))

        return data

    except Exception as e:
        print("Azure VM #", vmNum, " is bad")
        return False
