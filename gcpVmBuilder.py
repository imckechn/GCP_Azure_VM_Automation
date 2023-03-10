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

        print("Name: ", name)
        print("Image: ", image)
        print("Image Project: ", imageProject)
        print("Zone: ", zone)
        print("\n\n")

        print("Running it")
        # print(
        #     "gcloud compute instances create " + name +
        #     " --image=" + image +
        #     " --image-project=" + imageProject +
        #     " --zone=" + zone +
        #     " --machine-type=e2-medium" +
        #     " --boot-disk-size=10"
        # )
        os.system("gcloud compute instances create " + name +
                        " --image=" + image +
                        " --image-project=" + imageProject +
                        " --zone=" + zone +
                        " --machine-type=e2-medium" +
                        " --boot-disk-size=10"
        )

        return data

    except Exception as e:
        print("GCP VM #", vmNum, " is bad")
        return False

# gcloud compute instances create linuxserver01 
# --image=debian-10-buster-v20210916 
# --image-project=debian-cloud 
# --zone=northamerica-northeast2-a 
# --machine-type=e2-medium 
# --boot-disk-size=10 

