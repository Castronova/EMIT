import json
from sprint import *


class Connection(object):
    def __init__(self, title, url):

        self.title = title
        self.url = url
        self.network = None


def get_wof_json_as_dictionary():
    wof_json = get_wof_json_path()

    if not os.path.exists(wof_json):
        print("Path %s does not exist" % wof_json)
        return

    with open(wof_json, "r") as f:
        try:
            data = json.load(f)
        except ValueError:
            print "Failed to parse WOF json"
            data = {}
    return data


def get_wof_json_as_instances():
    """
    Turns the wof_sites.json into Connection objects
    :return: list(type(Connection))
    """

    data = get_wof_json_as_dictionary()
    if not len(data):
        sPrint("No wof sites found", messageType=MessageType.DEBUG)
        return []

    connections_list = []
    for title in data.keys():
        if not isinstance(data[title], dict):
            sPrint("Connections.get_wof_json_as_instances() expected a dictionary")
            return connections_list
        if "wsdl" in data[title] and "network" in data[title]:
            site = Connection(title=title, url=data[title]["wsdl"])
            site.network = data[title]["network"]
            connections_list.append(site)

    return connections_list


def get_wof_json_as_list():
    """
    Converts the wof_sites.json into a 2D list
    :return: list(type(list))
    """
    data = get_wof_json_as_dictionary()
    if not len(data):
        sPrint("No wof sites found", messageType=MessageType.DEBUG)
        return []

    connections_list = []
    for title in data.keys():
        if not isinstance(data[title], dict):
            sPrint("Connections.get_wof_json_as_instances() expected a dictionary")
            return connections_list
        if "wsdl" in data[title] and "network" in data[title]:
            site = [title, data[title]["network"], data[title]["wsdl"]]
            connections_list.append(site)

    return connections_list


def get_wof_json_path():
    current_directory = os.path.dirname(os.path.abspath(__file__))  # rename to current_directory
    wof_path = os.path.abspath(os.path.join(current_directory, '../../app_data/dat/wofsites.json'))

    if not os.path.exists(wof_path):
        sPrint("Path %s does not exist" % wof_path, messageType=MessageType.DEBUG)
        return

    return wof_path


