param([int]$Minutes = 5)

$branch = "develop"
if (-not (git rev-parse --verify $branch 2>$null)) {
  git checkout -B $branch
} else {
  git checkout $branch
}

function Get-HumanCommitMessage {
  $files = git diff --cached --name-only | Where-Object { $_ -ne '' }
  if (-not $files) { return "small updates" }
  $labels = New-Object System.Collections.Generic.List[string]
  foreach ($f in $files) {
    if ($f -like 'src/ui/*') { $labels.Add('UI') }
    elseif ($f -like 'src/core/*') { $labels.Add('pipeline') }
    elseif ($f -like 'tests/*') { $labels.Add('tests') }
    elseif ($f -like 'data/*') { $labels.Add('data') }
    elseif ($f -like 'reports/*') { $labels.Add('reports') }
    elseif ($f -like 'architecture_RM-ODP/*') { $labels.Add('architecture docs') }
    elseif ($f -like 'ai_approaches/*') { $labels.Add('ai approaches') }
    elseif ($f -like 'ai_research/*') { $labels.Add('ai research') }
    elseif ($f -like 'knowledge_exchange/*') { $labels.Add('comms') }
    elseif ($f -like 'market/*') { $labels.Add('market') }
    elseif ($f -like 'software/*' -or $f -like '.streamlit/*') { $labels.Add('dev/deploy') }
    elseif ($f -like '.gitignore' -or $f -like '.gitattributes') { $labels.Add('repo setup') }
    elseif ($f -like 'README.md') { $labels.Add('readme') }
    elseif ($f -like 'dev/*') { $labels.Add('dev tooling') }
  }
  $unique = $labels | Sort-Object -Unique
  if (-not $unique -or $unique.Count -eq 0) { return "small updates" }
  return ("update " + ($unique -join ", "))
}

while ($true) {
  Write-Host "Working for $Minutes minutes..."
  Start-Sleep -Seconds ($Minutes * 60)

  git add -A
  if (git diff --cached --quiet) {
    git push -u origin $branch 2>$null
  } else {
    $msg = Get-HumanCommitMessage
    git commit -m $msg
    git push -u origin $branch
  }

  $answer = Read-Host "Type 'c' to continue another $Minutes min; anything else to stop"
  if ($answer -ne 'c') { break }
}

