import equis, argparse, sys, os.path, subprocess

def main():
    args = parse_arguments()
    if args.no_fetch and args.no_merge:
        print("nothing to do")
        return

    if not args.all:
        projects = equis.read_config()['index']
    else:
        projects = list(equis.all_projects())

    projects.sort(key=lambda x:x["name"].lower())
    for x in projects:
        os.chdir(x['dir'])

        gs = git_status()
        if gs['error']:
            # not a git repo
            continue

        print("-- {} --".format(x['name']))
        if not args.no_fetch:
            fetch_changes()

        if not args.no_merge:
            merge_changes(gs['changes'])

        print()


def parse_arguments():
    parser = argparse.ArgumentParser(prog="equis git-pull",
        description='Step through each project and run git fetch and merge all updated branches.')
    parser.add_argument('--all', dest='all', action='store_true',
        help='include projects in the registered directories')
    parser.add_argument('--no-fetch', dest='no_fetch', action='store_true',
        help='do not run git fetch, only merge outdated branches')
    parser.add_argument('--no-merge', dest='no_merge', action='store_true',
        help='do not run git merge, only fetch from remotes')

    return parser.parse_args()


def fetch_changes():
    gf = git_fetch()
    if gf['output']:
        print(gf['output'])

    if gf['error']:
        print(RED("error fetching changes"))
        return


def merge_changes(has_local_changes):
    glrb = git_list_remote_branches()
    if glrb['error']:
        print(RED("error listing remote branches: ") + glrb['error'])
        return

    for branch in glrb['branches']:
        attempt_to_update_branch(branch, has_local_changes)


def attempt_to_update_branch(branch_data, has_local_changes):
    branch = branch_data['name']
    remote_branch = branch_data['remote']

    if git_is_branch_with_upstream(branch):
        print(GREEN(branch + ": up to date"))
        return

    if git_is_branch_ahead_of_upstream(branch):
        print(GREEN(branch + ": ahead of origin"))
        return


    if not git_can_ff_merge_branch(branch):
        print(YELLOW(branch +": out of date; update requires merge"))
        return

    if has_local_changes:
        print(YELLOW(branch + ": out of date; cannot update due to local changes"))
        return

    if git_is_branch_current(branch):
        gmfo = git_merge_ff_only()
    else:
        gmfo = git_merge_ff_only_on_a_different_branch(branch, remote_branch)

    if gmfo['error']:
        print(RED(branch+": out of date; failed to ff merge"))
    else:
        print(CYAN(branch+": updated"))

def git_fetch():
    result = {
        'error': False,
        'output': '',
    }

    proc = run_cmd_combined_output('git', 'fetch')
    result['output'] = proc.stdout.strip()
    if proc.returncode != 0:
        result['error'] = True

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


def git_list_remote_branches():
    result = {
        "error": None,
        "branches": [],
    }

    # \35 is the ascii group separator, which should be a safe separator here.
    proc = run_cmd('git', 'for-each-ref', '--format=%(refname:strip=2)\35%(upstream)', 'refs/heads/')
    if proc.stderr:
        result['error'] = proc.stderr
    elif proc.stdout:
        lines = proc.stdout.strip().split('\n')
        parts = [l.split('\35') for l in lines]
        for p in parts:
            if len(p) == 2 and p[1]:
                result['branches'].append({
                    'name': p[0],
                    'remote': p[1][13:],
                })

    return result


def git_is_branch_current(branch):
    proc = run_cmd('git', 'rev-parse', branch, 'HEAD')
    if proc.stderr or not proc.stdout:
        return False

    [main, upstream] = proc.stdout.strip().split('\n')
    return main == upstream

def git_is_branch_with_upstream(branch):
    proc = run_cmd('git', 'rev-parse', branch, branch+'@{upstream}')
    if proc.stderr or not proc.stdout:
        return False

    [main, upstream] = proc.stdout.strip().split('\n')
    return main == upstream

def git_is_branch_ahead_of_upstream(branch):
    proc = run_cmd('git', 'merge-base', '--is-ancestor', branch+'@{upstream}', branch)
    return proc.returncode == 0

def git_can_ff_merge_branch(branch):
    proc = run_cmd('git', 'merge-base', '--is-ancestor', branch, branch+'@{upstream}')
    return proc.returncode == 0

def git_merge_ff_only():
    result = {
        'error': False,
    }

    proc = run_cmd('git', 'merge', '--ff-only')
    if proc.returncode != 0:
        result['error'] = True

    return result

def git_merge_ff_only_on_a_different_branch(branch, remote):
    result = {
        'error': False,
    }

    # This is some black magic voodoo here.
    # http://stackoverflow.com/questions/3216360
    proc = run_cmd('git', 'fetch', '.', remote+":"+branch)
    if proc.returncode != 0:
        result['error'] = True
    return result


def run_cmd(*args):
    return subprocess.run(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)


def run_cmd_combined_output(*args):
    return subprocess.run(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)


def RED(s): return '\x1b[0;31m' + s + '\x1b[0m'
def YELLOW(s): return '\x1b[0;33m' + s + '\x1b[0m'
def GREEN(s): return '\x1b[0;32m' + s + '\x1b[0m'
def CYAN(s): return '\x1b[0;36m' + s + '\x1b[0m'


main()
