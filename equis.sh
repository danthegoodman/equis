[ "$0" = "$BASH_SOURCE" ] && { echo "equis.sh must be sourced"; exit 1 ; }
local equis_home="$(dirname "$BASH_SOURCE")/lib"
case "$1" in
  -yh) ;&
  --help) ;&
  help)
    echo "X - Equis, the project directory manager"
    echo
    echo "Commands"
    echo "  cd           jump to a directory"
    echo "  git-status   check for uncommitted or unpushed changes"
    echo "  open         opens a directory in an editor or IDE"
    echo
    echo "Managment"
    echo "  index        add a directory to the index"
    echo "  unindex      remove a directory from the index"
    echo "  register     add a directory to the registry"
    echo "  unregister   remove a directory from the registry"
    echo "  clean        remove non-existent directories from the index and registry"
    echo
    echo "Shortcuts"
    echo "  <nothing>    cd"
    echo "  --all        cd --all"
    echo "  a            cd --all"
    echo "  gst          git-status"
    return 1
    ;;

  "") ;&
  -*) ;&
  cd)
    source "$equis_home/cmd-cd.sh" "$@"
    ;;
  a)
    source "$equis_home/cmd-cd.sh" --all "$@"
    ;;

  gst) ;&
  git-status)
    shift
    bash "$equis_home/cmd-git-status.sh" "$@"
    ;;

  open)
    source "$equis_home/cmd-open.sh" "$@"
    ;;

  index) ;&
  unindex) ;&
  register) ;&
  unregister) ;&
  clean)
    local script="$1"
    shift
    python3 "$equis_home/cmd-${script}.py" "$@"
    ;;

  *)
    echo "Unknown command : $1"
    return 1
    ;;
esac
