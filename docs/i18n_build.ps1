# Build every language and (optionally) serve one for preview.
# Usage: .\i18n_build.ps1            # build all
#        .\i18n_build.ps1 -Serve en  # build all, then serve the en site on :8001
param([string]$Serve)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. refresh catalogs from current source
python -m sphinx -b gettext "$root/source" "$root/_build/gettext"
sphinx-intl update -p "$root/_build/gettext" -l en -d "$root/source/locale"

# 2. build each language into its own subfolder
foreach ($lang in @('zh_CN','en')) {
    python -m sphinx -b html -D language=$lang "$root/source" "$root/_build/html/$lang"
}

# 3. optional preview
if ($Serve) {
    Set-Location "$root/_build/html/$Serve"
    python -m http.server 8001 --bind 127.0.0.1
}
