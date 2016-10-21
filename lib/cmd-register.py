import equis, argparse, sys, os.path

def main():
    args = parse_arguments()
    new_item = build_registry_item(args)

    registry = equis.read_registry()
    old_item = update_registry(registry, new_item)
    equis.write_registry(registry)

    report_changes(new_item, old_item)

def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis register",
        description='Add directory to registry. ')
    parser.add_argument('directory',
        help='Target directory')
    parser.add_argument('-d', '--depth', dest='depth', required=True,
        help='The number of directories to traverse to reach projects.')
    return parser.parse_args()

def build_registry_item(args):
    target_dir = os.path.abspath(args.directory)

    if not os.path.isdir(target_dir):
        sys.exit("Unable to open directory "+target_dir)

    target_depth = int(args.depth)
    if target_depth < 0:
        sys.exit("Depth must 0 or greater")

    # TODO items exist at given depth

    return {
        'dir': target_dir,
        'depth':target_depth,
    }

def update_registry(registry, new_item):
    for ndx, item in enumerate(registry):
        if item["dir"] == new_item["dir"]:
            registry[ndx] = new_item
            return item

    registry.append(new_item)
    return None

def report_changes(new_item, old_item):
    print("Registered " + new_item['dir'])
    print("  Depth: {}".format(new_item['depth']))

    if old_item:
        print("")
        print("Previous Configuration")
        print("  Depth: {}".format(old_item['depth']))

main()
