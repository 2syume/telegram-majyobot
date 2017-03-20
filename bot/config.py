import configparser

config = configparser.RawConfigParser()
configFilePath = "config.ini"
config.read(configFilePath)
