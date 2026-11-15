# Owner-admin installation template only. NOT native-host accepted.
# Intended as ACTIONS_RUNNER_HOOK_JOB_STARTED in a protected runner service env.
$ErrorActionPreference = 'Stop'
$python = 'C:\Program Files\Python313\python.exe' # Admin must verify fixed interpreter
$gate = 'C:\CTOPSRunnerGate\admission.py'
$approvalDir = 'C:\CTOPSRunnerGate\approvals'
$limitMs = 15000

function Assert-AdminControlledPath([string] $Target, [bool] $IsDirectory) {
  $entry = Get-Item -LiteralPath $Target -Force -ErrorAction Stop
  if ([bool]$entry.PSIsContainer -ne $IsDirectory) { throw 'Wrong protected file type' }
  if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Reparse point rejected' }
  $current = $entry
  while ($null -ne $current) {
    if (($current.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Ancestor link rejected' }
    $acl = Get-Acl -LiteralPath $current.FullName -ErrorAction Stop
    $owner = $acl.GetOwner([Security.Principal.SecurityIdentifier]).Value
    if ($owner -notin @('S-1-5-18', 'S-1-5-32-544')) { throw 'Untrusted owner of protected path' }
    foreach ($ace in $acl.Access) {
      if ($ace.AccessControlType -ne [Security.AccessControl.AccessControlType]::Allow) { continue }
      $sid = $ace.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
      # Only SYSTEM and built-in Administrators may have mutation rights.
      if ($sid -in @('S-1-5-18', 'S-1-5-32-544')) { continue }
      $mutatingRights = [Security.AccessControl.FileSystemRights]::Write -bor
        [Security.AccessControl.FileSystemRights]::Modify -bor
        [Security.AccessControl.FileSystemRights]::Delete -bor
        [Security.AccessControl.FileSystemRights]::ChangePermissions -bor
        [Security.AccessControl.FileSystemRights]::TakeOwnership -bor
        [Security.AccessControl.FileSystemRights]::CreateFiles -bor
        [Security.AccessControl.FileSystemRights]::CreateDirectories -bor
        [Security.AccessControl.FileSystemRights]::DeleteSubdirectoriesAndFiles
      if (($ace.FileSystemRights -band $mutatingRights) -ne 0) { throw 'Untrusted write ACE in protected path' }
    }
    $current = $current.Parent
  }
}

$process = $null
try {
  foreach ($key in @('GITHUB_RUN_ID','GITHUB_RUN_ATTEMPT')) {
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($key))) { throw 'Missing run context' }
  }
  foreach ($key in @('GITHUB_JOB','RUNNER_NAME')) {
    $value = [Environment]::GetEnvironmentVariable($key)
    if ([string]::IsNullOrEmpty($value) -or $value -cnotmatch '^[A-Za-z0-9_-]{1,100}$') { throw 'Unsafe run context' }
  }
  if ($env:GITHUB_RUN_ID -cnotmatch '^[1-9][0-9]{0,18}$' -or $env:GITHUB_RUN_ATTEMPT -cnotmatch '^[1-9][0-9]{0,18}$') { throw 'Unsafe numeric context' }
  $permit = Join-Path -Path $approvalDir -ChildPath ("$($env:GITHUB_RUN_ID)-$($env:GITHUB_RUN_ATTEMPT)-$($env:GITHUB_JOB)-$($env:RUNNER_NAME).json")
  Assert-AdminControlledPath -Target $python -IsDirectory $false
  Assert-AdminControlledPath -Target $gate -IsDirectory $false
  Assert-AdminControlledPath -Target $approvalDir -IsDirectory $true
  Assert-AdminControlledPath -Target $permit -IsDirectory $false
  $process = Start-Process -FilePath $python -ArgumentList @('-I','-B',('"'+$gate+'"')) -NoNewWindow -PassThru
  if (-not $process.WaitForExit($limitMs)) {
    & "$env:SystemRoot\System32\taskkill.exe" /PID $process.Id /T /F | Out-Null
    throw 'Admission timed out'
  }
  if ($process.ExitCode -ne 0) { throw 'Admission rejected job' }
  Write-Output 'CTO_RUNNER_GATE_ALLOW: owner-file approved exact job'
  exit 0
} catch {
  if ($null -ne $process -and -not $process.HasExited) {
    & "$env:SystemRoot\System32\taskkill.exe" /PID $process.Id /T /F | Out-Null
  }
  Write-Output 'CTO_RUNNER_GATE_DENY: native hook approval failed'
  exit 64
}