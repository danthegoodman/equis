import equis, argparse, sys, os.path, distutils.spawn

def main():
    args = parse_arguments()
    new_item = build_index_item(args)

    config = equis.read_config()
    old_item = update_indexes(config['index'], new_item)
    equis.write_config(config)

    report_changes(new_item, old_item)

def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis index",
        description='Add directory to index')
    parser.add_argument('directory',
        help='Target directory')
    parser.add_argument('-n', '--name', dest='name', default='',
        help='Name of directory for searching. Defaults to the directory name.')
    parser.add_argument('-o', '--opener', dest='opener', default='',
        help='Optional command for opening this directory')

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

def update_indexes(indexes, new_item):
    for ndx, item in enumerate(indexes):
        if item["name"] == new_item["name"]:
            indexes[ndx] = new_item
            return item

    indexes.append(new_item)
    return None

def report_changes(new_item, old_item):
    print("Indexed " + new_item['name'])
    print("  Directory: " + new_item['dir'])
    if new_item['opener']:
        print("  Opener   : " + new_item['opener'])
    if old_item:
        print("")
        print("Previous Configuration")
        print("  Directory: " + old_item['dir'])
        if old_item['opener']:
            print("  Opener   : " + old_item['opener'])

main()
