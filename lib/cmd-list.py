import equis, argparse, sys, os.path

def main():
    args = parse_arguments()

    if not args.all:
        projects = equis.read_config()['index']
    else:
        projects = list(equis.all_projects())

    projects.sort(key=lambda x:x["name"].lower())
    for x in projects:
        print(x['dir'])

def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis list",
        description='List directories from the index or registry')
    parser.add_argument('--all', dest='all', action='store_true',
        help='Include directories in the registry')

    return parser.parse_args()

main()
