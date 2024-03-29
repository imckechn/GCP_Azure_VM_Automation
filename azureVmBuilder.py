# Import the needed credential and management objects from the libraries.
import datetime
import subprocess
import json
import os

keys = ['purpose', 'os', 'team']

azureKeyOptions = ["name", "n", "resource-group", "g", "availability-set", "boot-diagnostic-storage", "capacity-reservation-group",
        "crg", "computer-name", "count", "custom-date", "edge-zone", "enable-agent", "enable-auto-update", "enable-hotpatching", "enable-secure-boot",
        "enable-vtpm", "eviction-policy", "image", "license-type", "location", "l", "max-price", "no-wait", "patch-mode", "platform-fault-domain",
        "ppg", "priority", "secrets", "security-type", "size", "ssh-key-name", "tags", "user-data", "validate", "vmss", "zone", "z", "admin-password",
        "admin-username", "authentication-type", "generate-ssh-keys", "ssh-dest-key-path", "ssh-key-values", "host", "host-group", "assign-identity",
        "role", "scope", "plan-name", "plan-product", "plan-promotion-code", "plan-publisher", "workspace", "accelerated-networking", "asgs",
        "nic-delete-option", "nics", "nsg", "nsg-rule", "private-ip-address", "public-ip-address", "public-ip-address-allocation", "subnet",
        "public-ip-address-dns-name", "public-ip-sku", "subnet-address-prefix", "vnet-address-prefix", "vnet-name", "attach-data-disks", "attach-os-disk",
        "data-disk-caching", "data-disk-delete-option", "data-disk-encryption-sets", "data-disk-sizes-gb", "encryption-at-host", "ephemeral-os-disk",
        "ephemeral-os-disk-placement", "ephemeral-placement", "os-disk-caching", "os-disk-delete-option", "os-disk-delete-option",
        "os-disk-encryption-set", "os-disk-name", "os-disk-size-gb", "os-type", "specialized", "storage-account", "storage-container-name",
        "storage-sku", "ultra-ssd-enabled", "use-unmanaged-disk"]

# Handles building the azure VMs
def azureBuildVMs(vmNum, config):
    data = [vmNum]
    VMname = config['name']

    #Makes a string of all the azure VM configurations
    azureElements = ""
    for key, value in config.items():
        if key not in keys and key in azureKeyOptions:
            azureElements += " --" + key + " " + value

    #Get a string containing all the current VM names
    print("Running 'az vm list' to check if Azure VM named ", VMname, " already exists.")
    currentVms = json.loads(subprocess.run("az vm list", capture_output=True, shell=True, text=True).stdout)

    for vm in currentVms:
        if vm['name'] == VMname:
            print("Azure VM named ", VMname, " already exists.")
            return None

    try:
        data.append(config['purpose'])
        data.append(config['os'])
        data.append(config['team'])

        #Create the VM
        print("Running 'az vm create" + azureElements + "' to create an Azure VM")
        ans = subprocess.run("az vm create" + azureElements, capture_output=True, shell=True, text=True)

        #Check if the VM was created successfully
        if "stderr='ERROR" in str(ans) or "stderr='WARNING":
            print("Azure VM #", vmNum, " is bad")
            print("Error/Warning: ", ans.stderr)
        else:
            print("Created Azure VM #", vmNum)

        #Get the time the VM finished being created at
        data.append(str(datetime.datetime.now()))
        data.append(ans.stdout)

        return data

    except Exception as e:
        print("Azure VM #", vmNum, " is bad")
        return False

def azureOpenPorts():
    portNum = 0
    while(True):
        requestedPort = input("Enter the port number you want to open ")
        if requestedPort.isdigit():
            portNum = int(requestedPort)
            break

    print("You're current resource groups:")
    os.system("az group list -otable")

    resourceGroup = input("Enter the resource group you want to open the port in ")
    vmName = input("For which VM do you want to open the port ")

    #Open the port
    print("Running '" + "az vm open-port --port " + str(portNum)  + " --resource-group " + str(resourceGroup) + "' to open the port")
    ans = subprocess.run("az vm open-port --port " + str(portNum) + " --resource-group " + str(resourceGroup) + " --name " + str(vmName), capture_output=True, shell=True, text=True)

    if ans.stderr == "":
        print("Port", portNum, "is open")
    else:
        print("Port", portNum, "is not open")
        print("Error: ", ans.stderr)
