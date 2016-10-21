[[ $* == *-h* ]] && {
  echo "equis cd [-h] [--all]"
  echo
  echo "cd to a project directory using the fzf interactive finder"
  echo
  echo "By default, only projects from the index will be listed"
  echo
  echo "optional arguments:"
  echo "  -h, --help            show this help message and exit"
  echo "  --all                 include projects in the registered directories"
  return 1
}

local listType projects res

listType="index"
[[ $* == *--all* ]] && listType="all"

projects="$(python3 -S "$equis_home/fzf_list.py" "$listType" "")"
[[ $? == 0 ]] || return 1

res="$(echo "$projects" | fzf -d '@@@' --with-nth 2 --reverse --no-sort --preview 'bash "'"$equis_home/fzf_preview.sh"'" {}')"
[ -z "$res" ] && return 1

cd "$(echo "${res%@@@*}" | jq -r .dir)"
