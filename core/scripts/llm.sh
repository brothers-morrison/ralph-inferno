
"""
# .SYNOPSIS
#   Bash Wrapper function to less badly call into a python script for calling OPENROUTER
#
# .DESCRIPTION
#   Because Bash (is decidedly old and clunky), doublequotes will break this and royally HOSE us up here.
#   TBD: Fix this and escape all the things that will break BASH here
#       OR (BETTER)
#   Rewrite the program to not be in bash -- aka, start over with a different project, 
#   and/or get claude to rewrite this in a better language.
# .EXAMPLE
#   call from bash:>
#       llm_query "$query"
"""
local query="${1:-TEST1 what is 2 plus 4}"
python_cmd="python3"

function llm_query()
{
    local query2="${1:-TEST2 what is 8 plus 16}"
    $python_cmd "core/llm_client.py" "$query2"
}