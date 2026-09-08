$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$serverPath = Join-Path $PSScriptRoot 'tools\server.mjs'
& node $serverPath
exit $LASTEXITCODE
