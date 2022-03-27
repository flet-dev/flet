Remove-Item 'C:\go' -Recurse -Force

$goDistPath = "$env:TEMP\go$GO_VERSION.windows-amd64.zip"
(New-Object Net.WebClient).DownloadFile("https://golang.org/dl/go$($env:GO_VERSION).windows-amd64.zip", $goDistPath)
7z x $goDistPath -o"$env:SystemDrive\" | Out-Null

go version