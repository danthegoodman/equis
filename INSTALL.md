### Dependencies

* `python3`, which must be python 3.5 or greater
* [`fzf`](https://github.com/junegunn/fzf), which must be v0.13.0 or greater
* [`jq`](https://stedolan.github.io/jq/)


### Installation

```
git clone https://github.com/danthegoodman/equis
```

Add these lines to your `.bash_profile` or `.bashrc`:

```
export EQUIS_DIR=$HOME/.equis
x() { source "/path/to/equis/equis.sh" "$@"; }
```

`EQUIS_DIR` is the directory where you'd like to store the json files.
It will be created by equis.

`x` must be a function.
You can name it whatever you'd like.
Be sure to change the path to where you cloned this project.
