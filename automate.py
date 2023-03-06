import configparser

config = configparser.ConfigParser()

#filename = input("please Give a Azure or GCP conf file name: ")
filename = "azure01.conf"

config.read(filename)
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']