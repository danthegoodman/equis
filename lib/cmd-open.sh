[[ $* == *-h* ]] && {
  echo "equis open [-h] [--all]"
  echo
  echo "opens a project directory with its configured opener."
  echo
  echo "Only items in the index with an opener will be listed."
  echo
  echo "optional arguments:"
  echo "  -h, --help            show this help message and exit"
  return 1
}

local projects res

projects="$(python3 -S "$equis_home/fzf_list.py" "index" "opener")"
[[ $? == 0 ]] || return 1

res="$(echo "$projects" | fzf -d '@@@' --with-nth 2 --reverse --no-sort --preview 'bash "'"$equis_home/fzf_preview.sh"'" {}')"
[ -z "$res" ] && return 1

res="$(echo "${res%@@@*}" | jq -r '"\(.dir)@@@\(.opener)"')"
"${res#*@@@}" "${res%@@@*}"
