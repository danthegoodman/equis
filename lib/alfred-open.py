import equis, sys, json

def main(query):
    projects = [x for x in equis.read_indexes() if x["opener"]]
    projects = [x for x in projects if fuzzy_score(x, query)]

    projects.sort(key= lambda x: x["name"].lower())
    projects.sort(key= lambda x: x["score"])

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

def fuzzy_score(proj, query):
    name = proj['name'].lower()
    score = 0
    lastNdx = -1
    ndx = -1
    for c in query:
        ndx = name.find(c, ndx+1)
        if ndx == -1: return False
        if lastNdx >= 0:
            score += (ndx - lastNdx)
        lastNdx = ndx
    proj['score'] = score
    return True

main(sys.argv[1].lower())
