import dotenv
from linode_api4 import LinodeClient
import os

_client = None

def initialize_client():
    global _client
    if _client:
        return
    dotenv.load_dotenv()
    _client = LinodeClient(os.getenv("TOKEN"))


def get_regions():
    initialize_client()
    return [r for r in map(lambda r: r.id, _client.regions())]


def get_linodes():
    initialize_client()
    return [l for l in map(lambda l: l.ipv4[0], _client.linode.instances())]


def make_linode(region):
    initialize_client()
    linode, password = _client.linode.instance_create("g6-nanode-1", region, image="linode/debian11")
    return linode, password