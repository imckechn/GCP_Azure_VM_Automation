import datetime
import subprocess

keys = ["project", "team", "purpose", "os"]
gcpKeyOptions = ["accelerator", "type", "boot-disk-device-name", "boot-disk-provisioned-iops", "boot-disk-size",
        "create-disk", "description", "disk", "boot", "device-name", "mode", "name", "scope", "hostname", "ipv6-network-tier",
        "ipv6-public-ptr-domain", "labels", "local-ssd", "interface", "machine-type", "maintenance-policy", "metadata", "metadata-from-file",
        "min-cpu-platform", "min-node-cpu", "network", "network-interface", "network-tier", "private-ipv6-google-access-type",
        "private-network-ip", "resource-policies", "shielded-integrity-monitoring", "source-instance-template", "stack-type", "subnet", "tags",
        "threads-per-core", "zone", "address", "boot-disk-kms-key", "boot-disk-kms-keyring", "boot-disk-mks-location", "boot-disk-kms-project",
        "custom-cpu", "custom-memory", "custom-extensions", "custom-vm-type", "image-family-scope", "image-project", "image", "image-family",
        "source-snapshot", "node", "node-affinity-file", "node-group", "public-ptr-domain", "reservation", "reservation-affinity", "default",
        "scopes", "service-account"]

#Function to automate the building of the GCP VMs
def gcpBuildVMs(vmNum, config):
    data = [vmNum]
    vmName = config['name']

    #Gets a string of all the current VMs
    currentVMs = subprocess.run("gcloud compute instances list", capture_output=True, shell=True, text=True).stdout

    #Checks if the current vm already exists
    if vmName in currentVMs:
        print("GCP VM named ", vmName, " already exists")
        return None

    gcpElements = ""

    #Creates a string of all the VM configurations
    for key, value in config.items():
        if key == "imageproject":
            key = "image-project"

        if key not in keys and key in gcpKeyOptions:
            if key == 'name':
                gcpElements += value.lower()
            else:
                gcpElements += " --" + key + "=" + value

    try:
        data.append(config['project'])
        data.append(config['team'])
        data.append(config['purpose'])
        data.append(config['os'])

        #Create the VM
        print("Running 'gcloud compute instances create " + gcpElements)
        ans = subprocess.run("gcloud compute instances create " + gcpElements, capture_output=True, shell=True, text=True)

        #Check if the VM was created successfully
        if 'RUNNING' not in str(ans):
            print("GCP VM #", vmNum, " failed")
            print("Error: ", ans.stderr)
            return False
        else:
            data.append(ans.args)
            data.append(ans.returncode)
            data.append(ans.stdout)
            data.append(ans.stderr)
            print("Created GCP VM #", vmNum)

        #Get the time the VM finished being created at
        data.append(str(datetime.datetime.now()))
        data.append(str(datetime.datetime.now()))

        #Return the data which contains all the details about the VM
        return data

    except Exception as e:
        print(e)
        print("GCP VM #", vmNum, " is bad")
        return False

#This function handles  opening the ports on the GCP VMs
def gcpOpenPorts():
    portNum = 0
    while(True):
        requestedPort = input("Enter the port number you want to open ")
        if requestedPort.isdigit():
            portNum = int(requestedPort)
            break

    print("Running 'gcloud compute firewall-rules create allow-port-" + str(portNum) + " --allow tcp:" + str(portNum))
    ans = subprocess.run("gcloud compute firewall-rules create allow-port-" + str(portNum) + " --allow tcp:" + str(portNum), capture_output=True, shell=True, text=True)

    if "Created" in ans.stderr:
        print("Successfully opened port " + str(portNum))
    else:
        print("Error opening port " + str(portNum))
        print("Error: ", ans.stderr)