import equis, sys, json

if sys.argv[1] == "index":
    projects = equis.read_config()['index']
    if not projects:
        sys.exit("no projects have been indexed; (did you want --help?)")
elif sys.argv[1] == "all":
    projects = list(equis.all_projects())
    if not projects:
        sys.exit("no directories have been registered or indexed; (did you want --help?)")
else:
    sys.exit("unknown list command")

if sys.argv[2]:
    key_filter = sys.argv[2]
    projects = [x for x in projects if x[key_filter]]

projects.sort(key=lambda x:x["name"].lower())
for x in projects:
    print(json.dumps(x) + "@@@" + x["name"])
