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

def gcpBuildVMs(vmNum, config):
    data = [vmNum]

    gcpElements = ""
    for key, value in config.items():
        if key not in keys and key in gcpKeyOptions:
            if key == 'name':
                gcpElements += " --" + key + " " + value.lower()
            else:
                gcpElements += " --" + key + " " + value

    try:
        data.append(config['project'])
        data.append(config['team'])
        data.append(config['purpose'])
        data.append(config['os'])

        print("Running 'gcloud compute instances create" + gcpElements)
        ans = subprocess.run("Running 'gcloud compute instances create" + gcpElements, capture_output=True, shell=True, text=True)

        if 'stderr="ERROR' in str(ans):
            print("GCP VM #", vmNum, " is bad")
            return False
        else:
            print("Created GCP VM #", vmNum)

        #Get the time the VM finished being created at
        data.append(str(datetime.datetime.now()))

        return data

    except Exception as e:
        print(e)
        print("GCP VM #", vmNum, " is bad")
        return False