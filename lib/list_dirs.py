import equis, sys, json

if sys.argv[1] == "index":
    projects = equis.read_indexes()
    if not projects:
        sys.exit("no projects have been indexed; (did you want --help?)")
elif sys.argv[1] == "all":
    projects = list(equis.all_projects())
    if not projects:
        sys.exit("no directories have been registered or indexed; (did you want --help?)")
else:
    sys.exit("unknown list command")

projects.sort(key=lambda x:x["name"].lower())
for x in projects:
    print(x["dir"] + "@@@" + x["name"])
