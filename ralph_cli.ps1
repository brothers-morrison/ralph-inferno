<#
.SYNOPSIS
    Ralph CLI wrapper
#>

Param(
    $RALPH_DIR = ".ralph",
    $PATH_TO_PS1 = "scripts/ralph.ps1"
)

$RALPH_DIR = if(Test-Path($RALPH_DIR)){ "$RALPH_DIR"  }else{"$($env:RALPH_CLI)"}

Function Start-Ralph([System.Object[]] $args) {
    $full_path = $(Join-Path -Path $(Join-Path -Path "./" -ChildPath "$RALPH_DIR") -ChildPath "$PATH_TO_PS1")
    If(-Not(Test-Path($full_path)))
    {
        throw "$full_path does not exist, please try again."
    }
    & "$full_path" $args
}

Start-Ralph $args