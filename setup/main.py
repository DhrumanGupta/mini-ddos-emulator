import linode

def main():
    regions = linode.get_regions()
    print(f"[INFO]: Found {len(regions)} regions")
    
    linodes = linode.get_linodes()
    print(f"[INFO]: {len(linodes)} linodes are running")
    
    # print(linode.make_linode(regions[0]))
    # print(linode.get_linodes())


if __name__ == "__main__":
    main()