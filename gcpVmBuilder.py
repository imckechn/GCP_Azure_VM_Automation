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
    vmName = config['name']

    currentVMs = subprocess.run("gcloud compute instances list", capture_output=True, shell=True, text=True).stdout

    if vmName in currentVMs:
        print("GCP VM named ", vmName, " already exists")
        return None

    gcpElements = ""
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

        print("Running 'gcloud compute instances create " + gcpElements)
        ans = subprocess.run("gcloud compute instances create " + gcpElements, capture_output=True, shell=True, text=True)

        if 'stderr="ERROR' in str(ans):
            print("GCP VM #", vmNum, " is bad")
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

        return data

    except Exception as e:
        print(e)
        print("GCP VM #", vmNum, " is bad")
        return False


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