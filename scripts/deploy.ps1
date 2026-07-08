param(
  [string]$EnvFile = ".deploy.env"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $EnvFile)) {
  throw "Missing $EnvFile. Copy .deploy.env.example to .deploy.env and fill in the server details."
}

Get-Content $EnvFile | ForEach-Object {
  if ($_ -match "^\s*#" -or $_ -notmatch "=") { return }
  $name, $value = $_ -split "=", 2
  [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
}

$required = "SSH_HOST", "SSH_USER", "SSH_PORT", "REMOTE_PATH", "SSH_KEY"
foreach ($name in $required) {
  if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name))) {
    throw "Missing $name in $EnvFile."
  }
}

$sshKeyPath = Resolve-Path -LiteralPath $env:SSH_KEY -ErrorAction Stop

$package = "deploy-package.zip"
if (Test-Path $package) {
  Remove-Item $package
}

$items = @("passenger_wsgi.py", "public", "README.md")
Compress-Archive -Path $items -DestinationPath $package -Force

$sshTarget = "$($env:SSH_USER)@$($env:SSH_HOST)"
$sshArgs = @(
  "-i", $sshKeyPath.Path,
  "-p", $env:SSH_PORT,
  "-o", "IdentitiesOnly=yes",
  "-o", "BatchMode=yes"
)
$scpArgs = @(
  "-i", $sshKeyPath.Path,
  "-P", $env:SSH_PORT,
  "-o", "IdentitiesOnly=yes",
  "-o", "BatchMode=yes"
)

scp @scpArgs $package "${sshTarget}:/tmp/global-consult-release.zip"

$remoteCommand = @"
set -e
mkdir -p '$($env:REMOTE_PATH)'
unzip -o /tmp/global-consult-release.zip -d '$($env:REMOTE_PATH)'
mkdir -p '$($env:REMOTE_PATH)/tmp'
touch '$($env:REMOTE_PATH)/tmp/restart.txt'
rm -f /tmp/global-consult-release.zip
"@

ssh @sshArgs $sshTarget $remoteCommand
Write-Host "Deployed to $($env:SSH_HOST):$($env:REMOTE_PATH)"
