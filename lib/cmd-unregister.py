import equis, argparse, sys, os.path

def main():
    args = parse_arguments()
    target_dir = os.path.abspath(args.directory)

    config = equis.read_config()
    update_registry(config['registry'], target_dir)
    equis.write_config(config)

    print("Removed {} from the registry".format(target_dir))

def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis unregister",
        description='Remove directory from registry')
    parser.add_argument('directory',
        help='Directory to remove')
    return parser.parse_args()

def update_registry(indexes, target_dir):
    for ndx, item in enumerate(indexes):
        if item["dir"] == target_dir:
            indexes.pop(ndx)
            return

    sys.exit("No registered directory found: '{}'".format(target_dir))

main()
