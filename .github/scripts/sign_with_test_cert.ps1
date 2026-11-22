# Signs $env:FLET_EXE with the test certificate whose thumbprint is in
# $env:TEST_CERT_THUMBPRINT, and fails unless the executable was unsigned before
# and carries the test certificate's signature after.
# Requiring an unsigned executable means a signature left from an earlier step
# can't pass for this one. The certificate isn't trusted, so the status isn't
# "Valid"; what matters is that the executable can be signed at all.
$ErrorActionPreference = "Stop"

$exe = $env:FLET_EXE
$before = Get-AuthenticodeSignature -FilePath $exe
if ($before.Status -ne "NotSigned") {
    Write-Error "$exe must be unsigned before signing, but its signature status is $($before.Status): $($before.StatusMessage)"
}

$cert = Get-Item "Cert:\CurrentUser\My\$env:TEST_CERT_THUMBPRINT"
$result = Set-AuthenticodeSignature -FilePath $exe -Certificate $cert -ErrorAction SilentlyContinue -ErrorVariable signErrors
$after = Get-AuthenticodeSignature -FilePath $exe
$broken = @("NotSigned", "HashMismatch", "NotSupportedFileFormat", "Incompatible")
if ($after.SignerCertificate.Thumbprint -ne $cert.Thumbprint -or $broken -contains $after.Status) {
    $reason = if ($signErrors) { $signErrors -join "; " } elseif ($result) { $result.StatusMessage } else { $after.StatusMessage }
    Write-Error "Could not sign ${exe} (status $($after.Status)): $reason"
}
Write-Host "Signed $exe with the test certificate"
