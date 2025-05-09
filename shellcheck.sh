#!/bin/bash
exit_code=0
while IFS= read -r -d '' file
do
    shellcheck --severity=info "$file";
    tsitkai="$?"
    exit_code=$(( tsitkai != 0 ? tsitkai : exit_code))
done <   <(find . -type f -name '*.sh' -not -path './venv/*' -print0)
exit $(( exit_code == 0 ? 0 : 1))
