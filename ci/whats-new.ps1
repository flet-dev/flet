$milestone = 12

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Fetch issues from GitHub
$issues = Invoke-RestMethod "https://api.github.com/repos/flet-dev/flet/issues?state=all&per_page=100&milestone=$($milestone)&sort=created&direction=asc"

# Prepare an array with sorting
$sortedIssues = $issues | ForEach-Object {
    $isBug = 0
    foreach ($label in $_.labels) {
        if ($label.name -eq 'bug') {
            $isBug = 1
        }
    }
    [PSCustomObject]@{
        Issue  = $_
        IsBug  = $isBug  # Sorting key: 0 for non-bug, 1 for bug
    }
} | Sort-Object IsBug  # Sort: Non-bug first, bug last

# Output sorted issues
foreach ($item in $sortedIssues) {
    $issue = $item.Issue
    $prefix = ""

    foreach ($label in $issue.labels) {
        if ($label.name -eq 'bug') {
            $prefix = "Fixed: "
        }
    }

    $title = $issue.title.replace('fix: ', '')

    "* $prefix$($title) ([#$($issue.number)]($($issue.html_url)))"
}