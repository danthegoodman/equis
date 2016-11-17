import equis, sys, json

def main(query):
    projects = [x for x in equis.read_config()['index'] if x["opener"]]
    projects = [x for x in projects if fuzzy_find(x, query)]

    projects.sort(key= lambda x: x["name"].lower())

    items = [build_item(x) for x in projects]
    print(json.dumps({"items":items}))

def build_item(proj):
    return {
        'uid': proj['dir'],
        'title': proj['name'],
        'subtitle': proj['dir'],
        'arg': proj['opener'] + "@@@" + proj['dir'],
        'icon': 'public.folder',
        'autocomplete': proj['name'],
        'quicklookurl': 'file://'+proj['dir'],
    }

def fuzzy_find(proj, query):
    name = proj['name'].lower()
    all_words = query.split(" ")

    for word in all_words:
        ndx = -1
        for c in word:
            ndx = name.find(c, ndx+1)
            if ndx == -1: return False

    return True

main(sys.argv[1].lower())
