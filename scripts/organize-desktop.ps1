$ErrorActionPreference = 'Continue'
$desktop = [Environment]::GetFolderPath('Desktop')

$portfolio = Join-Path $desktop ([char]0x4F5C + [char]0x54C1 + [char]0x96C6)
$projects  = Join-Path $desktop ([char]0x5F00 + [char]0x53D1 + [char]0x9879 + [char]0x76EE)
$school    = Join-Path $desktop ([char]0x5B66 + [char]0x6821 + [char]0x6587 + [char]0x6863)
$export    = Join-Path $desktop '01-导出文件'
$tools     = Join-Path $desktop '01-工具'
$shortcuts = Join-Path $desktop ([char]0x5FEB + [char]0x6377 + [char]0x65B9 + [char]0x5F0F)

foreach ($path in @($portfolio, $projects, $school, $export, $tools, $shortcuts)) {
    if ($path) { New-Item -ItemType Directory -Force -Path $path | Out-Null }
}

$resumeDir = Join-Path $school '2220048-秦艺榕\求职简历'
$archiveDir = Join-Path $export '归档-投递备份'
New-Item -ItemType Directory -Force -Path $resumeDir, $archiveDir | Out-Null

Get-ChildItem -LiteralPath $desktop -File -Filter '*.pdf' -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.Name -match '秦艺榕|CEO|产品|项目') {
        $dest = Join-Path $resumeDir $_.Name
        if (-not (Test-Path -LiteralPath $dest)) {
            Move-Item -LiteralPath $_.FullName -Destination $dest -ErrorAction SilentlyContinue
        }
    }
}

Get-ChildItem -LiteralPath $desktop -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like '*投递*' } | ForEach-Object {
    $dest = Join-Path $archiveDir $_.Name
    if (-not (Test-Path -LiteralPath $dest)) {
        Move-Item -LiteralPath $_.FullName -Destination $dest -ErrorAction SilentlyContinue
    }
}

Get-ChildItem -LiteralPath $desktop -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like '*对话*' -and $_.Name -like '*ai*' } | ForEach-Object {
    $dest = Join-Path $projects '项目-ai视觉对话'
    if (-not (Test-Path -LiteralPath $dest)) {
        Move-Item -LiteralPath $_.FullName -Destination $dest -ErrorAction SilentlyContinue
    }
}

Get-ChildItem -LiteralPath $desktop -File -Filter '*.lnk' -ErrorAction SilentlyContinue | ForEach-Object {
    $dest = Join-Path $shortcuts $_.Name
    if (-not (Test-Path -LiteralPath $dest)) {
        Move-Item -LiteralPath $_.FullName -Destination $dest -ErrorAction SilentlyContinue
    }
}

Write-Host OK
