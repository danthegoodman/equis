import equis, argparse, sys

def main():
    args = parse_arguments()

    config = equis.read_config()
    update_indexes(config['index'], args.name)
    equis.write_config(config)

    print("Removed {} from the index".format(args.name))

def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis unindex",
        description='Remove directory from index')
    parser.add_argument('name',
        help='Name of the item to remove')
    return parser.parse_args()

def update_indexes(indexes, name):
    for ndx, item in enumerate(indexes):
        if item["name"] == name:
            indexes.pop(ndx)
            return

    sys.exit("No item found with name: '{}'".format(name))

main()
