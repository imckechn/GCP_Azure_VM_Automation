import os

def gcpBuildVMs(vmNum, config):
    data = [vmNum]

    try:
        name = config['name']
        image = config['image']
        imageProject = config['imageproject']

        if imageProject == 'debian-cloud':
            imageProject = 'debian'
        zone = config['zone']

        data.append(config['project'])
        data.append(config['team'])
        data.append(config['purpose'])
        data.append(config['os'])

        os.system("gcloud compute instances create " + name +
                        " --machine-type " + image +
                        " --image-family " + imageProject +
                        "--image-project " + imageProject +
                        " --zone " + zone
        )

        return data

    except Exception as e:
        print("Azure VM #", vmNum, " is bad")
        return False
