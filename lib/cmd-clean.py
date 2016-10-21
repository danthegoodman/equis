import equis, argparse, sys, os.path

def main():
    parse_arguments()
    indexes = equis.read_indexes()
    registry = equis.read_registry()

    new_indexes = update_indexes(indexes)
    new_registry = update_registry(registry)

    equis.write_indexes(new_indexes)
    equis.write_registry(new_registry)

def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis clean",
        description='Remove non-existent directories from the index and registry')
    return parser.parse_args()

def build_index_item(args):
    target_dir = os.path.abspath(args.directory)

    if not os.path.isdir(target_dir):
        sys.exit("Unable to open directory "+target_dir)

    target_name = args.name or os.path.basename(target_dir)

    target_opener = ""
    if args.opener:
        target_opener = distutils.spawn.find_executable(args.opener)
        if not target_opener:
            sys.exit("Unable to locate opener on path: "+args.opener)

    return {
        'name':target_name,
        'dir': target_dir,
        'opener': target_opener
    }

def update_indexes(indexes):
    new_result = []
    for item in indexes:
        if os.path.exists(item["dir"]):
            new_result.append(item)
        else:
            print("Removing from index: {}".format(item['dir']))
    return new_result

def update_registry(registry):
    new_result = []
    for item in registry:
        if os.path.exists(item["dir"]):
            new_result.append(item)
        else:
            print("Removing from registry: {}".format(item['dir']))
    return new_result

main()
