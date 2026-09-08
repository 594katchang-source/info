param(
    [string]$MetadataUpdatedAt = ''
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$appRoot = $PSScriptRoot
$datasetUrl = 'https://data.fda.gov.tw/data/opendata/export/20/json'
$temporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("nutrirank-refresh-" + [guid]::NewGuid().ToString('N'))
$archivePath = Join-Path $temporaryRoot '20_5.json.zip'
$extractPath = Join-Path $temporaryRoot 'source'
$generatedPath = Join-Path $temporaryRoot 'nutrition_data.js'
$targetPath = Join-Path $appRoot 'nutrition_data.js'
$transformerPath = Join-Path $appRoot 'tools\transform-tfda-data.mjs'
$validatorPath = Join-Path $appRoot 'tools\validate-tfda-data.mjs'

try {
    New-Item -ItemType Directory -Path $temporaryRoot | Out-Null

    Write-Host 'Downloading the official TFDA dataset...'
    Invoke-WebRequest -Uri $datasetUrl -OutFile $archivePath

    Write-Host 'Extracting source data...'
    Expand-Archive -LiteralPath $archivePath -DestinationPath $extractPath
    $sourceJson = Get-ChildItem -LiteralPath $extractPath -Filter '*.json' -File -Recurse | Select-Object -First 1
    if (-not $sourceJson) {
        throw 'The official ZIP did not contain a JSON file.'
    }

    Write-Host 'Transforming and validating data...'
    & node $transformerPath $sourceJson.FullName $generatedPath $MetadataUpdatedAt
    if ($LASTEXITCODE -ne 0) {
        throw "Data transformer failed with exit code $LASTEXITCODE."
    }

    & node $validatorPath $sourceJson.FullName $generatedPath
    if ($LASTEXITCODE -ne 0) {
        throw "Data validation failed with exit code $LASTEXITCODE."
    }

    Move-Item -LiteralPath $generatedPath -Destination $targetPath -Force
    $hash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash
    Write-Host "Updated: $targetPath"
    Write-Host "SHA-256: $hash"
}
finally {
    $resolvedTempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    $resolvedTarget = [System.IO.Path]::GetFullPath($temporaryRoot)
    $leaf = Split-Path -Leaf $resolvedTarget
    if ($resolvedTarget.StartsWith($resolvedTempBase, [System.StringComparison]::OrdinalIgnoreCase) -and $leaf.StartsWith('nutrirank-refresh-')) {
        Remove-Item -LiteralPath $resolvedTarget -Recurse -Force -ErrorAction SilentlyContinue
    }
}
