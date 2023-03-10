import datetime
∂import subprocess

def gcpBuildVMs(vmNum, config):
    data = [vmNum]

    try:
        name = config['name']
        image = config['image']
        imageProject = config['imageproject']
        zone = config['zone']

        data.append(config['project'])
        data.append(config['team'])
        data.append(config['purpose'])
        data.append(config['os'])

        print("Running 'gcloud compute instances create " + name.lower() +
                        " --image=" + image +
                        " --image-project=" + imageProject +
                        " --zone=" + zone +
                        "' to create a GCP VM"
        )
        ans = subprocess.run("gcloud compute instances create " + name.lower() +
                        " --image=" + image +
                        " --image-project=" + imageProject +
                        " --zone=" + zone,
                        capture_output=True, shell=True, text=True
        )

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