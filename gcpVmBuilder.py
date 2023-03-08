import os

def buildVMs(vmNum, config):
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


        ans = os.system()

        return data

    except Exception as e:
        print("Azure VM #", vmNum, " is bad")
        return False
