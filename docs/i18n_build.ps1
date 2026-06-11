# Build every language and (optionally) serve one for preview.
# Usage: .\i18n_build.ps1            # build all
#        .\i18n_build.ps1 -Serve en  # build all, then serve the en site on :8001
param([string]$Serve)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. refresh catalogs from current source
python -m sphinx -b gettext "$root/source" "$root/_build/gettext"
sphinx-intl update -p "$root/_build/gettext" -l en -d "$root/source/locale"

# 2. build each variant × language into its own subfolder.
#    -d writes doctrees OUTSIDE the html dir so .doctrees never ships.
$variants = @{ 'offline' = @(); 'online' = @('-t','online') }
foreach ($variant in $variants.Keys) {
    foreach ($lang in @('zh_CN','en')) {
        python -m sphinx -b html @($variants[$variant]) -d "$root/_build/doctrees/$variant/$lang" `
            -D language=$lang "$root/source" "$root/_build/html/$variant/$lang"
    }
}

# 3. optional preview
if ($Serve) {
    Set-Location "$root/_build/html/offline/$Serve"
    python -m http.server 8001 --bind 127.0.0.1
}
