[[ $* == *-h* ]] && {
  echo "cmd-git-status.sh [-h] [-v] [--all]"
  echo
  echo "Check git status for directories."
  echo
  echo "By default, only projects with uncommitted or unpushed changes"
  echo "in the index will be listed"
  echo
  echo "optional arguments:"
  echo "  -h, --help            show this help message and exit"
  echo "  -v, --verbose         show status of all included projects"
  echo "  --all                 include projects in the registered directories"
  exit 1
}
[[ $* == *-v* ]] && VERBOSE=1
[[ $* == *--all* ]] && ALL=1

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
RESET=$(tput sgr0)
EQUIS_HOME="$(dirname "$0")"

function main(){
  local LIST_TYPE="index"
  [[ $ALL ]] && LIST_TYPE="all"

  local PROJECTS=()
  mapfile -t PROJECTS < <(python3 "$EQUIS_HOME/list_dirs.py" "$LIST_TYPE")
  for D in "${PROJECTS[@]}"; do
    (
      cd "${D%@@@*}" || exit
      printLocalChanges "${D#*@@@}"
    )
  done
}

function printLocalChanges(){
  local BRANCHES=() OUTPUT=()
  local B COUNT STATUS
  local NAME=$1

  local GIT_STATUS="$(git status --porcelain 2>&1)"
  if [[ "$GIT_STATUS" == "fatal:"* ]] ; then
    if [[ $VERBOSE ]]; then
      OUTPUT+=("${RED}not a git repo${RESET}")
    fi
  else
    if [[ -n "$GIT_STATUS" ]] ; then
      OUTPUT+=("contains ${YELLOW}uncommited changes${RESET}")
    fi

    eval "$(git for-each-ref --shell --format='BRANCHES+=(%(refname))' refs/heads/)"
    for B in "${BRANCHES[@]}"; do
      B="${B:11}"
      COUNT="$(git rev-list --count "${B}@{u}...${B}" 2>&1)"
      if [[ "$COUNT" == *"no upstream"* ]] ; then
        if [[ "$B" == master && $VERBOSE ]] ; then
          OUTPUT+=("${RED}no remotes${RESET}")
        fi
        HAS_REMOTE=0
        COUNT="$(git rev-list --count "master..${B}")"
        STATUS="${GREEN}not on master"
      elif ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
        echo "$COUNT"
        COUNT=-1
        STATUS="${RED}[[error]]"
      else
        HAS_REMOTE=1
        STATUS="${RED}not pushed"
      fi

      if [[ 0 -ne "$COUNT" ]] ; then
        OUTPUT+=("$B : $COUNT commits ${STATUS}${RESET}")
      elif [[ $VERBOSE ]] ; then
        if [[ 1 -eq "$HAS_REMOTE" ]]; then
          OUTPUT+=("$B : up to date")
        else
          OUTPUT+=("$B : merged into master")
        fi
      fi
    done
  fi

  if [[ 0 -ne ${#OUTPUT[@]} ]] ; then
    echo "-- $NAME --"
    for B in "${OUTPUT[@]}"; do
      echo "$B"
    done
    echo
  elif [[ $VERBOSE ]] ; then
    echo "-- $NAME --"
    echo "unknown"
    echo
  fi
}

main
