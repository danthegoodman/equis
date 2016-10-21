import os, sys, json, errno

if sys.version_info < (3,5):
    v = sys.version_info
    sys.exit('Python v3.5+ is required; Running v{}.{}'.format(v.major, v.minor))

equis_dir = os.environ.get('EQUIS_DIR')
if not equis_dir:
    sys.exit('Missing environment variable EQUIS_DIR')

def read_indexes():
    return _read_or_create_json('index.json')

def read_registry():
    return _read_or_create_json('registry.json')

def write_indexes(data):
    _write_json('index.json', data)

def write_registry(data):
    _write_json('registry.json', data)

def all_projects():
    indexes = read_indexes()
    registry = read_registry()

    yield from indexes
    dirs = set(x['dir'] for x in indexes) | set(x['dir'] for x in registry)

    for regitem in read_registry():
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

    # level = reg_item['depth']
    # print >>sys.stderr, '---{} ({})---'.format(reg_item['dir'], level)
    # for root, dirs, files in os.walk(reg_item['dir'], topdown=True, followlinks=True):
    #     if level >= 0:
    #         print >>sys.stderr, root
    #         print >>sys.stderr, dirs
    #     else:
    #         break
    #     level-=1
    # return []


def _read_or_create_json(filename):
    target_file = equis_dir + '/' + filename

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
        target.write('[]')
        target.close()
        return []

def _write_json(filename, data):
    target_file = equis_dir + '/' + filename

    with open(target_file, 'w') as fp:
        return json.dump(data, fp)
