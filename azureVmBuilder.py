# Import the needed credential and management objects from the libraries.
import datetime
import subprocess

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

def azureBuildVMs(vmNum, config):
    data = [vmNum]

    azureElements = ""
    for key, value in config.items():
        if key not in keys and key in azureKeyOptions:
            azureElements += " --" + key + " " + value

    print("\n")
    try:
        data.append(config['purpose'])
        data.append(config['os'])
        data.append(config['team'])


        print("Running 'az vm create" + azureElements + "' to create an Azure VM")
        ans = subprocess.run("az vm create" + azureElements, capture_output=True, shell=True, text=True)

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
