import digitalocean
import os
import dotenv
from threading import Event

dotenv.load_dotenv()

_manager = digitalocean.Manager(token=os.getenv("DO_TOKEN"))

def create(region, name="Example"):
    event = Event()
    droplet = digitalocean.Droplet(token=os.getenv("DO_TOKEN"),
                               name=name,
                               region='blr1',
                            image="125549412",
                               size_slug='s-1vcpu-1gb',  # 1GB RAM, 1 vCPU
                               ssh_keys=_manager.get_all_sshkeys(), # Automatically add my SSH key
                               )

    droplet.create()
    event.wait(30)
    droplet.load()
    while not droplet.ip_address:
        droplet.load()
        event.wait(5)
    
    return [droplet.id, '', droplet.ip_address]

def delete_all():
    for droplet in _manager.get_all_droplets():
        if str(droplet.id) == "337346095":
            continue 
        droplet.destroy()

def get_regions():
    return ['nyc1', 'nyc3', 'ams3', 'sfo3', 'sgp1', 'lon1', 'fra1', 'tor1', 'blr1', 'syd1']