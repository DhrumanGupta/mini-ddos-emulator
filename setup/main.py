import datetime
import random
from time import sleep
import dotenv
import linode as linode_api
import os 
import pandas as pd
from sys import argv
import requests

csv_path = 'linodes_data.csv'

def debug(msg):
    print(f"{datetime.now().strftime('%H:%M:%S')} * {msg}")

def delete():
    linodes = linode_api.get_linodes_raw()
    print(f"[INFO]: Deleting {len(linodes)} linodes")
    for linode in linodes:
        linode.delete()


def create(n=35):
    # print("x")
    regions = linode_api.get_regions()
    print(f"[INFO]: Found {len(regions)} regions")
    
    linodes = linode_api.get_linodes()
    print(f"[INFO]: {len(linodes)} linodes are running")

    new_linodes = []
    if len(linodes) <= 0:
        for i in range(n):
            lin, pwd = linode_api.make_linode(regions[i % len(regions)], 1059469, {"SERVER_IP_ADDRESS": os.getenv('SERVER_IP')})
            new_linodes.append([lin.id, pwd])

        print(new_linodes)

        linodes = linode_api.get_linodes()
        for i in range(len(new_linodes)):
            id = new_linodes[i][0]
            for linode in linodes:
                if linode['id'] == id:
                    new_linodes[i].append(linode['ip'])
                    break

        df = pd.DataFrame(new_linodes, columns=['Id', 'Password', 'IP'])
        df.to_csv(csv_path, index=False)
    
    # print(linode.get_linodes())

def run():
    data = pd.read_csv(csv_path)
    if len(data) != 35:
        debug(f"[ERROR]: Expected 35 linodes, found {len(data)}")
        return
    
    seconds_before_attack = random.randint(5*60, 6*60) # 5-6 minutes
    attack_duration_seconds = random.randint(5*60, 7*60) # 5-7 minutes
    
    real_clients = []
    compromised_clients = []

    for i in range(30):
        real_clients.append(data.iloc[i]['IP'])
    
    for i in range(30, 35):
        compromised_clients.append(data.iloc[i]['IP'])

    debug(f"[INFO]: Real clients loaded")
    debug(f"[INFO]: Starting real client simulation, will start attack in {seconds_before_attack} seconds")

    for ip in real_clients:
        requests.get(f"http://{ip}/emulate-user?time={seconds_before_attack*1000}")
    
    debug(f"[INFO]: User requests started, waiting {seconds_before_attack} seconds before attack")

    sleep(seconds_before_attack)

    debug(f"[INFO]: Starting attack..")

    converted = []
    for i in range(9, -1, -1):
        ip = random.choice(real_clients)
        real_clients.remove(ip)
        converted.append(ip)
    
    for i in converted:
        requests.get(f"http://{i}/stop-user")
        requests.get(f"http://{ip}/stop-malicious-user")
        compromised_clients.append(i)

    for ip in compromised_clients:
        requests.get(f"http://{ip}/emulate-malicious-user?time={attack_duration_seconds*1000}")

    debug(f"[INFO]: Attack started, waiting {attack_duration_seconds} seconds before stopping attack")
    sleep(attack_duration_seconds)

    debug("[INFO]: Stopping attack..")

    for ip in compromised_clients:
        requests.get(f"http://{ip}/stop-malicious-user")
        requests.get(f"http://{i}/stop-user")

    debug(f"[INFO]: Attack stopped")


options = {
    "delete": delete,
    "create": create,
    "run": run
}


def main():
    dotenv.load_dotenv()
    if len(argv) < 2:
        print(f"No arguments given. Options are {', '.join(options.keys())}")
        return
    
    command = argv[1]
    if command not in options.keys():
        print(f"Invalid command. Options are {', '.join(options.keys())}")
        return
    
    options[command]()


if __name__ == "__main__":
    main()