import equis, argparse, sys, os.path, subprocess

def main():
    args = parse_arguments()

    if not args.all:
        projects = equis.read_config()['index']
    else:
        projects = list(equis.all_projects())

    projects.sort(key=lambda x:x["name"].lower())
    for x in projects:
        os.chdir(x['dir'])
        output = read_changes(args.verbose)
        if output:
            print("-- {} --".format(x['name']))
            for o in output:
                print(o)
            print()
        elif args.verbose:
            print("-- {} --".format(x['name']))
            print("unknown")
            print()



def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis git-status",
        description='Check git status for directories. ')
    parser.add_argument('--all', dest='all', action='store_true',
        help='include projects in the registered directories')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help='show status of all included projects')
    return parser.parse_args()

def read_changes(verbose):
    result = []

    gst = git_status()
    if gst['error']:
        if verbose:
            result.append(RED("not a git repo"))
        return result

    if gst['changes']:
        result.append("contains " + YELLOW("uncommitted changes"))

    branches = git_list_branches()
    if branches['error']:
        result.append(RED(branches['error']))

    for br in branches['branches']:
        result.extend(read_branch_changes(verbose, br))

    return result


def read_branch_changes(verbose, br):
    result = []
    gcuc = git_count_upstream_commits(br)

    if gcuc['error']:
        result.append("{} : [error] {}".format(br, RED(gcuc['error'])))
        return result

    has_changes = False
    if gcuc['upstream']:
        has_changes = True
        result.append("{} : {} commits {}".format(br, gcuc['upstream'], GREEN("upstream")))

    if gcuc['local']:
        has_changes = True
        result.append("{} : {} commits {}".format(br, gcuc['local'], YELLOW("not pushed")))

    if gcuc['no_upstream']:
        if br == 'master':
            has_changes = True
            if verbose:
                result.append(RED("no remotes"))
        else:
            lc = git_count_local_commits(br)

            if lc['error']:
                result.append("{} : [error] {}".format(br, RED(lc['error'])))

            if lc['count']:
                has_changes = True
                result.append("{} : {} commits {}".format(br, lc['count'], CYAN('not on master')))

    if not has_changes and verbose:
        if gcuc['no_upstream']:
            result.append(br + " : merged into master")
        else:
            result.append(br + " : up to date")

    return result


def git_status():
    result = {
        'error': False,
        'changes': False,
    }

    proc = run_cmd('git', 'status', '--porcelain')
    if proc.returncode != 0:
        result['error'] = True
    elif proc.stdout:
        result['changes'] = True

    return result


def git_list_branches():
    result = {
        "error": None,
        "branches": [],
    }

    proc = run_cmd('git', 'for-each-ref', '--format=%(refname:strip=2)', 'refs/heads/')
    if proc.stderr:
        result['error'] = proc.stderr
    elif proc.stdout:
        result['branches'] = proc.stdout.strip().split('\n')

    return result


def git_count_upstream_commits(branch):
    result = {
        "error": None,
        "no_upstream": False,
        "upstream": 0,
        "local": 0,
    }

    proc = run_cmd('git', 'rev-list', '--left-right', '--count', branch+'@{u}...'+branch)
    parts = proc.stdout.split('\t')

    if "no upstream" in proc.stderr:
        result['no_upstream'] = True
    elif proc.stderr:
        result['error'] = proc.stderr
    elif len(parts) != 2:
        result['error'] = "invalid result"
    else:
        result['upstream'] = int(parts[0])
        result['local'] = int(parts[1])

    return result


def git_count_local_commits(branch):
    result = {
        "error": None,
        "count": 0,
    }

    proc = run_cmd('git', 'rev-list', '--count', 'master..'+branch)
    if proc.stderr:
        result['error'] = proc.stderr
    else:
        result['count'] = int(proc.stdout)

    return result


def run_cmd(*args):
    return subprocess.run(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)


def RED(s): return '\x1b[0;31m' + s + '\x1b[0m'
def YELLOW(s): return '\x1b[0;33m' + s + '\x1b[0m'
def GREEN(s): return '\x1b[0;32m' + s + '\x1b[0m'
def CYAN(s): return '\x1b[0;36m' + s + '\x1b[0m'

main()
