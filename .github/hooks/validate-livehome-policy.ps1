$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$issues = New-Object System.Collections.Generic.List[string]
$shouldBlock = $false

function Add-Issue([string] $message) {
    $script:issues.Add($message)
}

function Test-Needle([string] $path, [string[]] $needles, [string] $message) {
    if (-not (Test-Path $path)) {
        return
    }

    foreach ($needle in $needles) {
        if (Select-String -Path $path -SimpleMatch -Pattern $needle -Quiet) {
            Add-Issue $message
            return
        }
    }
}

function Get-GitAddedLines([string] $relativePath) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        return @()
    }

    $diff = & git -C $root diff --unified=0 -- $relativePath 2>$null
    if (-not $diff) {
        return @()
    }

    return $diff |
        Where-Object { $_ -like '+*' -and $_ -notlike '+++' } |
        ForEach-Object { $_.Substring(1) }
}

function Get-GitChangedFiles([string] $globPattern) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        return @()
    }

    $files = & git -C $root diff --name-only -- $globPattern 2>$null
    if (-not $files) {
        return @()
    }

    return $files | Where-Object { $_ }
}

function Get-AllGitChangedFiles() {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        return @()
    }

    $files = & git -C $root diff --name-only 2>$null
    if (-not $files) {
        return @()
    }

    return $files | Where-Object { $_ }
}

function Get-AllGitStatusFiles() {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        return @()
    }

    $files = & git -C $root status --porcelain --untracked-files=all 2>$null
    if (-not $files) {
        return @()
    }

    return $files |
        Where-Object { $_ -and $_.Length -ge 4 } |
        ForEach-Object {
            $candidate = $_.Substring(3)
            if ($candidate -like '* -> *') {
                $candidate = $candidate.Split(' -> ')[1]
            }
            $candidate
        } |
        Where-Object { $_ }
}

function Get-BusinessRootHits([string[]] $relativePaths) {
    $hits = New-Object System.Collections.Generic.List[string]
    foreach ($path in $relativePaths) {
        if ($path -like 'livehome_admin/*') {
            $hits.Add('backend')
            continue
        }
        if ($path -like 'livehome_app/*') {
            $hits.Add('app')
            continue
        }
        if ($path -like 'livehome_ng/*') {
            $hits.Add('web')
            continue
        }
    }
    return $hits | Select-Object -Unique
}

function Invoke-WorkspaceGuard([string] $scriptPath, [string] $rootPath) {
    if (-not (Test-Path $scriptPath)) {
        return @()
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        return @(@{ path = 'scripts/ai_workspace_guard.py'; code = 'python_missing'; severity = 'warning'; message = 'python is missing; workspace guard could not run' })
    }

    $raw = & $python.Source $scriptPath validate-changed --root $rootPath --json 2>$null
    if (-not $raw) {
        return @()
    }

    $rawText = [string]::Join("`n", $raw)

    try {
        $report = $rawText | ConvertFrom-Json
    } catch {
        return @(@{ path = 'scripts/ai_workspace_guard.py'; code = 'guard_parse_failed'; severity = 'warning'; message = 'workspace guard returned invalid JSON output' })
    }

    if (-not $report.issues) {
        return @()
    }

    return @($report.issues)
}

function Invoke-MarkdownGuard([string] $scriptPath, [string] $rootPath) {
    if (-not (Test-Path $scriptPath)) {
        return @()
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        return @(@{ path = 'scripts/ai_workspace_guard.py'; code = 'python_missing'; severity = 'warning'; message = 'python is missing; markdown guard could not run' })
    }

    $raw = & $python.Source $scriptPath validate-markdown --root $rootPath --json 2>$null
    if (-not $raw) {
        return @()
    }

    $rawText = [string]::Join("`n", $raw)

    try {
        $report = $rawText | ConvertFrom-Json
    } catch {
        return @(@{ path = 'scripts/ai_workspace_guard.py'; code = 'markdown_guard_parse_failed'; severity = 'warning'; message = 'markdown guard returned invalid JSON output' })
    }

    if (-not $report.issues) {
        return @()
    }

    return @($report.issues)
}

$githubPath = Join-Path $root ".github"
$webInstructions = Join-Path $githubPath "instructions\web.instructions.md"
$backendInstructions = Join-Path $githubPath "instructions\backend.instructions.md"
$architectAgent = Join-Path $githubPath "agents\architect.agent.md"
$flutterAgent = Join-Path $githubPath "agents\flutter.agent.md"
$angularAgent = Join-Path $githubPath "agents\angular.agent.md"
$promptsPath = Join-Path $githubPath "prompts"
$apiGovernancePrompt = Join-Path $promptsPath "api-governance-audit.prompt.md"
$workspaceGuard = Join-Path $root "scripts\ai_workspace_guard.py"

$githubMarkdown = Get-ChildItem -Path $githubPath -Recurse -File -Include *.md -ErrorAction SilentlyContinue
foreach ($file in $githubMarkdown) {
    if (Select-String -Path $file.FullName -Pattern 'code, msg, data' -SimpleMatch -Quiet) {
        Add-Issue ".github docs still contain code, msg, data; use code, message, data consistently"
        break
    }
}

Test-Needle -path $architectAgent -needles @(
    '#tool:vscode/askQuestions'
) -message "architect.agent.md still uses legacy #tool:vscode/askQuestions syntax; prefer vscode/askQuestions only when clarification is required"

Test-Needle -path $angularAgent -needles @(
    '#tool:vscode/askQuestions'
) -message "angular.agent.md still uses legacy #tool:vscode/askQuestions syntax; prefer vscode/askQuestions only when clarification is required"

Test-Needle -path $flutterAgent -needles @(
    '#tool:vscode/askQuestions'
) -message "flutter.agent.md still uses legacy #tool:vscode/askQuestions syntax; prefer vscode/askQuestions only when clarification is required"

Test-Needle -path $backendInstructions -needles @(
    '权限点统一命名为 `admin.{module}.{resource}.{action}`',
    '任何历史接口整改都必须先执行 `.github/prompts/api-governance-audit.prompt.md`'
) -message "backend.instructions.md is missing required admin API governance rules"

Test-Needle -path $webInstructions -needles @(
    'Service + RxJS BehaviorSubject',
    '{name}.module.ts',
    'params: any',
    'Observable<any>',
    'constructor(private http: HttpClient) {}',
    '${this.base}/save',
    '${this.base}/details',
    '${this.base}/remove',
    '${this.base}/batch_remove',
    '${this.base}/set'
) -message "web.instructions.md contains outdated Angular patterns; keep Standalone + OnPush + inject + typed service"

if (-not (Test-Path $apiGovernancePrompt)) {
    Add-Issue ".github/prompts/api-governance-audit.prompt.md is missing"
}

$workspaceGuardIssues = Invoke-WorkspaceGuard -scriptPath $workspaceGuard -rootPath $root
foreach ($issue in ($workspaceGuardIssues | Select-Object -First 8)) {
    Add-Issue "file-safety: $($issue.path) [$($issue.code)] $($issue.message)"
}

$statusChangedFiles = Get-AllGitStatusFiles
$changedMarkdownFiles = $statusChangedFiles | Where-Object { $_ -like '*.md' }
if ($changedMarkdownFiles.Count -gt 0) {
    $markdownGuardIssues = Invoke-MarkdownGuard -scriptPath $workspaceGuard -rootPath $root
    foreach ($issue in ($markdownGuardIssues | Select-Object -First 8)) {
        $message = "markdown-safety: $($issue.path) [$($issue.code)] $($issue.message)"
        if ($issue.severity -eq 'error') {
            $message = "$message；必须按对应 Markdown 类型重新写入并重新执行 validate-markdown，禁止继续覆盖原文"
        }
        Add-Issue $message
        if ($issue.severity -eq 'error') {
            $script:shouldBlock = $true
        }
    }
}

$apiAdminAddedLines = Get-GitAddedLines 'livehome_admin/routes/api_admin.php'
$apiAppAddedLines = Get-GitAddedLines 'livehome_admin/routes/api.php'
$changedFiles = if ($statusChangedFiles.Count -gt 0) { $statusChangedFiles } else { Get-AllGitChangedFiles }
$businessRootHits = Get-BusinessRootHits $changedFiles

if ($businessRootHits.Count -gt 1) {
    Add-Issue "changed files span multiple business roots ($($businessRootHits -join ', ')); split backend/app/web code changes by role or route them back through architect"
    $script:shouldBlock = $true
}

if ($apiAdminAddedLines | Where-Object { $_ -match '/[a-z0-9]+_[a-z0-9_/\-]*' }) {
    Add-Issue "new admin routes contain underscore paths; use kebab-case and document compatibility in api-contract"
}

if ($apiAdminAddedLines | Where-Object { $_ -match '/(save|details|remove|set|batch_remove|batch_delete)\b' }) {
    Add-Issue "new admin routes still use legacy save/details/remove/set style paths; mark compatibility or deprecated explicitly if retained"
}

if ($apiAppAddedLines | Where-Object { $_ -match '/(save|details|remove|set|delete|update|list|batch_remove|batch_delete)\b' }) {
    Add-Issue "new Flutter/App routes still use legacy action-style or list alias paths; prefer resource paths with HTTP semantics"
}

if ($apiAppAddedLines | Where-Object { $_ -match '/[a-z0-9]+_[a-z0-9_/\-]*' }) {
    Add-Issue "new Flutter/App routes contain underscore paths; use REST resource paths with kebab-case"
}

$tasksRoot = Join-Path $root "docs\tasks"
if (Test-Path $tasksRoot) {
    Get-ChildItem -Path $tasksRoot -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne '_templates' } |
        ForEach-Object {
            $taskDir = $_
            $hasAnyTask = @('backend.md', 'app.md', 'web.md') |
                ForEach-Object { Test-Path (Join-Path $taskDir.FullName $_) } |
                Where-Object { $_ } |
                Select-Object -First 1

            if ($hasAnyTask -and -not (Test-Path (Join-Path $taskDir.FullName 'api-contract.md'))) {
                Add-Issue "tasks/$($taskDir.Name) is missing api-contract.md"
            }
        }

    $changedTaskContracts = Get-GitChangedFiles 'tasks/*/api-contract.md'
    foreach ($relativeContractPath in $changedTaskContracts) {
        if ($relativeContractPath -match 'tasks/(_templates|api-governance-reset)/') {
            continue
        }

        $contractPath = Join-Path $root $relativeContractPath
        if (-not (Test-Path $contractPath)) {
            continue
        }

        $contractContent = Get-Content -Path $contractPath -Raw -ErrorAction SilentlyContinue
        if (-not $contractContent) {
            continue
        }

        $hasRequestTable = $contractContent -match '请求参数表|参数名 \| 类型 \| 必填 \| 位置 \| 说明'
        $hasResponseTable = $contractContent -match '响应字段表|字段路径 \| 类型 \|'
        $hasJsonExample = $contractContent -match 'JSON 响应示例|```json'

        if (-not ($hasRequestTable -and $hasResponseTable -and $hasJsonExample)) {
            Add-Issue "$relativeContractPath is missing field-level contract details; add request table, response table, and JSON example before frontend handoff"
        }
    }
}

$result = @{ continue = (-not $shouldBlock) }
if ($issues.Count -gt 0) {
    $preview = $issues | Select-Object -Unique | Select-Object -First 6
    $headline = if ($shouldBlock) { "LiveHome policy blocked tool execution:" } else { "LiveHome policy check:" }
    $result.systemMessage = "$headline`n- $($preview -join "`n- ")"
}

$result | ConvertTo-Json -Compress -Depth 4
