# Grimo model-specific Codex CLI launcher.
# Usage: .\scripts\codex-grimo.ps1 -Model Sol
#        .\scripts\codex-grimo.ps1 -Model Astra
#        .\scripts\codex-grimo.ps1 -Model Sol resume --last
# This is opt-in. The Codex Desktop model picker does not run this script.
[CmdletBinding()]
param(
    [ValidateSet('Astra', 'Sol')]
    [string]$Model = 'Sol',

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CodexArgs
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$presetsPath = Join-Path $repoRoot '.codex/context-presets.json'
$presets = Get-Content -LiteralPath $presetsPath -Raw -Encoding UTF8 | ConvertFrom-Json
$preset = $presets.PSObject.Properties[$Model].Value
if ($null -eq $preset) { throw "Unknown Codex context preset: $Model" }

Push-Location $repoRoot
try {
    & codex -m $preset.model `
        -c "model_context_window=$($preset.model_context_window)" `
        -c "model_auto_compact_token_limit=$($preset.model_auto_compact_token_limit)" `
        -c 'model_auto_compact_token_limit_scope="total"' `
        @CodexArgs
} finally {
    Pop-Location
}
