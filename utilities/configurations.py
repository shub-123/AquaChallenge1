import configparser

def getConfig():
    config = configparser.ConfigParser()
    config.read('utilities/properties.ini')
    return config


def get_host_url():
    host_url = {
        'host_url': getConfig()['API']['endpoint']
    }
    return host_url["host_url"]

def get_host_resouces():
    host_resources = {
        'host_resource1': getConfig()['Resources']['Resource1'],
        'host_resource2': getConfig()['Resources']['Resource2']

    }
    return host_resources


def get_jsondata(taskname, completion_status):
    body = {
        "task": taskname,
        "completed": completion_status
    }
    return body

def modify_json():
    body = {
        "task": "Modified Value",
        "completed": "false"
    }
    return body
