$milestone = 7

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
#Invoke-RestMethod https://api.github.com/repos/appveyor/ci/milestones
$issues = Invoke-RestMethod "https://api.github.com/repos/flet-dev/flet/issues?state=all&per_page=100&milestone=$($milestone)&sort=created&direction=asc"

$itemLabels = @{}

foreach ($issue in $issues) {

    $prefix = ""

    foreach ($label in $issue.labels) {
        if ($label.name -eq 'bug') {
            $prefix = "Fixed: "
            #break
        }
    }

    $title = $issue.title.replace('fix: ', '')

    #"$($issue.html_url) $prefix$($issue.title)"
    "* $prefix$($title) ([#$($issue.number)]($($issue.html_url)))"
}