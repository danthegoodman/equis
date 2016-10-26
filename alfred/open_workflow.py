#!/usr/bin/env python3
import plistlib, uuid, os, os.path, sys, distutils.spawn, zipfile, subprocess

if 'EQUIS_DIR' not in os.environ:
    sys.exit("Missing environment variable 'EQUIS_DIR'")

WORKFLOW_KEYWORD = "x"
UID_INPUT_FILTER = str(uuid.uuid4())
UID_ACTION_OPEN = str(uuid.uuid4())

EQUIS_DIR = os.environ['EQUIS_DIR']
EQUIS_HOME = os.path.realpath(os.path.join(sys.path[0], '..'))
PYTHON_EXEC = distutils.spawn.find_executable('python3')

def main():
    pl = build_plist()
    with zipfile.ZipFile('/tmp/equis.alfredworkflow', 'w') as zf:
        zf.writestr("info.plist", plistlib.dumps(pl))

    subprocess.run(["open", "/tmp/equis.alfredworkflow"])

def build_readme():
    return (
        "If the following parameters have changed, regenerate this workflow.\n"
        "\n"
        "EQUIS_DIR={}\n"
        "EQUIS_HOME={}\n"
        "Python 3 Bin={}\n"
    ).format(EQUIS_DIR, EQUIS_HOME, PYTHON_EXEC)

def build_script_input():
    alfred_script = os.path.join(EQUIS_HOME, 'lib/alfred-open.py')
    return (
        'export EQUIS_DIR="{}"\n'
        '"{}" "{}" "$1"\n'
    ).format(EQUIS_DIR, PYTHON_EXEC, alfred_script)

def build_script_open():
    opener = '"${1%@@@*}"'
    target = '"${1#*@@@}"'
    return opener + ' ' + target + '\n'

def build_plist():
    return {
        'bundleid': 'us.kirchmeier.equis',
        'createdby': 'Danny Kirchmeier',
        'description': 'the project directory manager',
        'disabled': False,
        'name': "equis",
        'readme': build_readme(),
        'webaddress': "https://github.com/danthegoodman/equis",
        'objects': [
            {
                'type': "alfred.workflow.input.scriptfilter",
                'uid': UID_INPUT_FILTER,
                'version': 2,
                'config': {
                    'keyword': WORKFLOW_KEYWORD,
                    'title': "Equis Open",
                    'runningsubtext': "Loading",
                    'script': build_script_input(),

                    'alfredfiltersresulsts': False,
                    'argumenttype': 1,
                    'escaping': 68,
                    'queuedelaycustom': 3,
                    'queuedelayimmediatelyinitially': True,
                    'queuedelaymode': 0,
                    'queuemode': 2,
                    'scriptargtype': 1, # argv
                    'scriptfile': "",
                    'subtext': "",
                    'type': 0,
                    'withspace': True,
                },
            },
            {
                'type': "alfred.workflow.action.script",
                'uid': UID_ACTION_OPEN,
                'verion': 2,
                'config': {
                    'script': build_script_open(),

                    'concurrently': False,
                    'escaping': 127,
                    'scriptargtype': 1, #argv
                    'scriptfile': "",
                    'type': 0,
                },
            },
        ],
        'connections': {
            UID_INPUT_FILTER: [
                {
                    'destinationuid': UID_ACTION_OPEN,
                    'modifiers': 0,
                    'modifiersubtext': '',
                    'vitoclose': False,
                },
            ]
        },
        'uidata': {
            UID_INPUT_FILTER: {
                'xpos': 290,
                'ypos': 150,
            },
            UID_ACTION_OPEN: {
                'xpos': 490,
                'ypos': 150,
            }
        },
    }

main()
