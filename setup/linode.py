from linode_api4 import LinodeClient, StackScript
import os

_client = None

def initialize_client():
    global _client
    if _client:
        return
    _client = LinodeClient(os.getenv("TOKEN"))


def get_regions():
    initialize_client()
    return [r for r in map(lambda r: r.id, _client.regions())]


def get_linodes():
    initialize_client()
    return [l for l in map(lambda l: {"ip": l.ipv4[0], "id": l.id}, _client.linode.instances())]


def get_linodes_raw():
    initialize_client()
    return _client.linode.instances()


def make_linode(region, stackscript, stackscript_data):
    initialize_client()
    # if (stackscript):
    #     stackscript = StackScript(stackscript)
    linode, password = _client.linode.instance_create("g6-nanode-1", region, image="linode/debian11", stackscript=stackscript, stackscript_data=stackscript_data)
    return linode, password