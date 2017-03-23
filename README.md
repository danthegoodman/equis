# X - Equis, the project directory manager

You tell Equis where your projects are.

It helps you navigate and manage them.

To Install, see [INSTALL.md](INSTALL.md).

### Getting Started - The Index

First, you probably have a project or two that you use all of the time.
Your frequently used projects are stored in the "index".

```bash
~$ x index ~/open_source/react
~$ x index ~/internal/auth/login-page
~$ x index ~/internal/auth/login-backend
```

Once you have added projects to the index, you can quickly jump to a project:

```bash
~$ x
# at this point, the fuzzy finder "fzf" takes over.
# Select a project and...
~/internal/login-page$ # boom. You've changed directories.
```

Equis can also open projects if you want to get into your editor or IDE quickly.

```bash
~$ x index ~/open_source/react -o atom
~$ x index ~/internal/auth/login-page -o webstorm
~$ x open
# at this point, the fuzzy finder "fzf" takes over and lists only the
# the projects with an opener. Select a project and...
~$ # boom. The tool will open.
```

Equis can also check to see if you have unpushed changes in your projects.

```bash
-- login-page --
contains uncommitted changes
master : 1 commits not pushed

-- login-backend --
contains uncommitted changes
fix/bug-3823 : 2 commits not on master
```

### Getting Started - The Registry

You might also have a few projects that are on your machine that you don't use very often.

You tell Equis where these projects are by storing the parent directory in the "registry".
The required `--depth` parameter tells Equis how deep your projects are tree.

```
~$ tree .
|-- open_source/
|   |-- angular
|   |-- jquery
|   |-- react
|-- internal/
|   |-- auth/
|   |   |-- login-backend
|   |   |-- login-page
|   |-- photos/
|   |   |-- image-uploader
|   |   |-- image-resizer
| ...   

~$ x register ~/open_source --depth 0
~$ x register ~/internal --depth 1
```

Now, you can invoke `x` with the `--all` flag to change to any of these projects:

```
# change directories
~$ x --all
# fzf takes over and list a _lot_ more projects now. Every project in the
# registered directories and those in the index.
```

Similarly, you can check all of these project's for unpushed changes.

```
~$ x git-status --all
# likewise.
```

# Documentation

```text
$ x --help
X - Equis, the project directory manager
Version 1.1.0

Commands
  cd           jump to a directory
  git-status   check for uncommitted or unpushed changes
  open         opens a directory in an editor or IDE

Management
  index        add a directory to the index
  unindex      remove a directory from the index
  register     add a directory to the registry
  unregister   remove a directory from the registry
  list         list all directories indexed or registered
  clean        remove non-existent directories from the index and registry

Shortcuts
  <nothing>    cd
  --all        cd --all
  a            cd --all
  gst          git-status
```

All commands accept a `--help` flag for additional details.

### Pronunciation

`EH:kees`. Equis is Spanish for the letter "X".

# Alfred

If you use and pay for [Alfred](https://www.alfredapp.com/), a workflow is available for the `open` command.

Run the `alfred/open_workflow.py` script in this project.

# Advanced Usage - Scripting

Equis provides the `list` and `list --all` commands to dump indexed and registered directories to standard out.
You can use this to perform a custom action over your projects:

```bash
x list | while read PROJ; do
  [[ -d "$PROJ/.git" ]] && echo "$PROJ :: has git repo" || echo "$PROJ :: not in git"
done
```
