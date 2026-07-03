param(
    [string]$VaultRoot = (Join-Path $HOME "vincci-knowledge-vault")
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SetupScript = Join-Path $ScriptDir "scripts/setup_vault.py"

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $Python) {
    throw "Python 3.7+ is required."
}

if ($Python.Name -eq "py.exe") {
    & $Python.Source -3 $SetupScript --vault $VaultRoot
} else {
    & $Python.Source $SetupScript --vault $VaultRoot
}
