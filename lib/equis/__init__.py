import os, sys, json, errno

if sys.version_info < (3,5):
    v = sys.version_info
    sys.exit('Python v3.5+ is required; Running v{}.{}'.format(v.major, v.minor))

equis_dir = os.environ.get('EQUIS_DIR')
if not equis_dir:
    sys.exit('Missing environment variable EQUIS_DIR')

def read_config():
    json = _read_or_create_json()
    if 'index' not in json:
        json['index'] = []
    if 'registry' not in json:
        json['registry'] = []
    return json

def write_config(data):
    target_file = equis_dir + '/config.json'

    with open(target_file, 'w') as fp:
        return json.dump(data, fp)

def all_projects():
    config = read_config()
    indexes = config["index"]
    registry = config["registry"]

    yield from indexes
    dirs = set(x['dir'] for x in indexes) | set(x['dir'] for x in registry)

    for regitem in registry:
        level = regitem['depth']
        currdirs = [regitem['dir']]
        nextdirs = []
        while level >= 0:
            for cd in currdirs:
                for entry in os.scandir(cd):
                    if entry.is_file(): continue
                    if entry.path in dirs: continue
                    dirs.add(entry.path)
                    if level <= 0:
                        yield {'name':entry.name, 'dir':entry.path}
                    else:
                        nextdirs.append(entry.path)
            currdirs = nextdirs
            nextdirs = []
            level -= 1

def _read_or_create_json():
    target_file = equis_dir + '/config.json'
    try:
        with open(target_file, 'r') as fp:
            return json.load(fp)
    except EnvironmentError as e:
        if getattr(e, 'errno', 0) != errno.ENOENT:
            raise e

        try:
            os.makedirs(equis_dir)
        except EnvironmentError as e:
            if getattr(e, 'errno', 0) != errno.EEXIST:
                raise e

        target = open(target_file, 'w')
        target.write('{}')
        target.close()
        return {}
