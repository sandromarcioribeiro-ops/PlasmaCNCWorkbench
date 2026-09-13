$ErrorActionPreference = "Stop"

$source = Split-Path -Parent $MyInvocation.MyCommand.Path
$freeCadRoot = Join-Path $env:APPDATA "FreeCAD"
$modRoots = @(
    (Join-Path $freeCadRoot "v1-1\Mod"),
    (Join-Path $freeCadRoot "Mod")
)

if (-not (Test-Path -LiteralPath (Join-Path $freeCadRoot "v1-1"))) {
    $modRoots = @((Join-Path $freeCadRoot "Mod"))
}

$items = @(
    "Init.py",
    "InitGui.py",
    "package.xml",
    "README.md",
    "LICENSE",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "example_mach3_catarina.py",
    "plasma_cnc",
    "resources"
)

foreach ($modRoot in $modRoots) {
    $target = Join-Path $modRoot "PlasmaCNCWorkbench"
    New-Item -ItemType Directory -Force -Path $modRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $target | Out-Null

    foreach ($item in $items) {
        $from = Join-Path $source $item
        $to = Join-Path $target $item
        if (Test-Path -LiteralPath $from -PathType Container) {
            robocopy $from $to /E /XD __pycache__ /XF *.pyc | Out-Null
            if ($LASTEXITCODE -gt 7) {
                throw "Falha ao copiar $from para $to"
            }
        } else {
            Copy-Item -LiteralPath $from -Destination $to -Force
        }
    }

    Write-Host "PlasmaCNCWorkbench instalado em: $target"
}

Write-Host "Reinicie o FreeCAD e escolha a bancada: Plasma CNC"
