# Signs $env:FLET_EXE with the test certificate whose thumbprint is in
# $env:TEST_CERT_THUMBPRINT, and fails when no signature was written.
# The certificate isn't trusted, so the status isn't "Valid"; what matters is
# that the executable can be signed at all.
$ErrorActionPreference = "Stop"

$cert = Get-Item "Cert:\CurrentUser\My\$env:TEST_CERT_THUMBPRINT"
$result = Set-AuthenticodeSignature -FilePath $env:FLET_EXE -Certificate $cert -ErrorAction Continue
$signature = Get-AuthenticodeSignature -FilePath $env:FLET_EXE
if (-not $signature.SignerCertificate) {
    Write-Error "Could not sign ${env:FLET_EXE}: $($result.StatusMessage)"
    exit 1
}
Write-Host "Signed $env:FLET_EXE with the test certificate"
