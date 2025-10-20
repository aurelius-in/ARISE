param([int]$Minutes = 5)

$branch = "develop"
if (-not (git rev-parse --verify $branch 2>$null)) {
  git checkout -B $branch
} else {
  git checkout $branch
}

while ($true) {
  Write-Host "Working for $Minutes minutes..."
  Start-Sleep -Seconds ($Minutes * 60)

  git add -A
  if (git diff --cached --quiet) {
    git push -u origin $branch 2>$null
  } else {
    $msg = "chore: checkpoint $(Get-Date -Format yyyy-MM-dd_HH-mm)"
    git commit -m $msg
    git push -u origin $branch
  }

  $answer = Read-Host "Type 'c' to continue another $Minutes min; anything else to stop"
  if ($answer -ne 'c') { break }
}

