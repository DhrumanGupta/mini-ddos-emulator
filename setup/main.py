import dotenv
import linode as linode_api
import os 
import pandas as pd
from sys import argv


def delete():
    linodes = linode_api.get_linodes_raw()
    print(f"[INFO]: Deleting {len(linodes)} linodes")
    for linode in linodes:
        linode.delete()


def main():
    # print("x")
    regions = linode_api.get_regions()
    print(f"[INFO]: Found {len(regions)} regions")
    
    linodes = linode_api.get_linodes()
    print(f"[INFO]: {len(linodes)} linodes are running")

    new_linodes = []
    if len(linodes) <= 0:
        for i in range(1):
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
        df.to_csv('linodes_data.csv', index=False)
    
    # print(linode.get_linodes())


if __name__ == "__main__":
    dotenv.load_dotenv()
    if len(argv) > 1 and argv[1] == 'delete':
        delete()
    else:
        main()