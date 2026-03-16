from typing import Optional
import requests
import re


def is_github_url(url: str) -> bool:
    """
    Check if the provided URL is a valid GitHub repository URL.

    Args:
        url (str): The URL to check.
    Returns:
        bool: True if the URL is a valid GitHub repository URL, False otherwise.
    """

    expected_prefixes = ("gh:", "https://github.com/", "http://github.com/")
    return url.startswith(expected_prefixes)


def get_owner_and_repo_from_url(url: str) -> Optional[tuple[str, str]]:
    """
    Extract the owner and repository name from a valid GitHub URL.

    Args:
        url (str): The URL to extract from.
    Returns:
        Optional[tuple[str, str]]: A tuple of (owner, repo) if valid, otherwise None.
    """
    expected_prefixes = ("gh:", "https://github.com/", "http://github.com/")

    # Step 1: Strip the matched prefix from the URL
    path = None
    for prefix in expected_prefixes:
        if url.startswith(prefix):
            path = url[len(prefix) :]  # Extract the remaining part after the prefix
            break

    # If no prefix matched, it's not a valid URL
    if path is None:
        return None

    # .strip("/") removes any trailing/leading slashes before splitting
    parts = path.strip("/").split("/")

    # A valid GitHub repo needs at least an owner and a repo name
    if len(parts) < 2:
        return None

    owner = parts[0]
    repo = parts[1]

    # remove '.git' suffix if present
    if repo.endswith(".git"):
        repo = repo[:-4]

    # Ensure neither owner nor repo is empty (e.g., in case of double slashes "owner//repo")
    if not owner or not repo:
        return None

    return owner, repo


def get_github_branches(
    owner: str, repo: str, token: Optional[str] = None
) -> list[str] | None:
    """
    Retrieve a list of all branches for a specified GitHub repository.

    Args:
        owner (str): The repository owner (username or organization name).
        repo (str): The repository name.
        token (str, optional): GitHub Personal Access Token (used for
        accessing private repos or increasing API rate limits).

    Returns:
        list: A list containing the names of all branches.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"

    # Set up request headers
    headers = {"Accept": "application/vnd.github.v3+json"}

    # Add Authorization header if a token is provided
    if token:
        headers["Authorization"] = f"Bearer {token}"

    branches = []
    page = 1

    while True:
        params = {"per_page": 100, "page": page}

        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code != 200:
            return None  # fail silently

        data = response.json()

        # If there is no data on the current page, pagination is complete. Exit the loop.
        if not data:
            break

        # Extract branch names from the current page and add them to the list
        for branch_info in data:
            branches.append(branch_info["name"])

        page += 1

    return branches


def get_latest_version_branch(
    branch_list: list[str], 
    target_version: Optional[str] = None
) -> Optional[str]:
    """
    Filters the branch list to strictly match 'x.x.x' format (e.g., 0.83.0),
    and returns the branch with the highest version number.
    If target_version is provided, it returns the highest version branch that
    is less than or equal to the target_version.

    Args:
        branch_list (list): A list of branch name strings.
        target_version (str, optional): The maximum version allowed (e.g., "0.83.0").
    Returns:
        str: The branch name with the highest version number, or None if no
        valid branches are found.
    """
    # Define a strict Regex pattern for 'x.x.x' where x is one or more digits
    pattern = re.compile(r"^\d+\.\d+\.\d+$")

    def version_key(version_str: str) -> tuple[int, ...]:
        # Extracts digits from the version string and converts to a tuple of ints
        # Using isdigit() prevents ValueError if target_version contains text (e.g., '0.83.dev0')
        return tuple(int(x) for x in version_str.split(".") if x.isdigit())

    valid_branches = [branch for branch in branch_list if pattern.match(branch)]

    if not valid_branches:
        return None

    if target_version:
        target_key = version_key(target_version)
        valid_branches = [
            branch for branch in valid_branches 
            if version_key(branch) <= target_key
        ]

    # Return None if the list becomes empty after applying the target_version limit
    if not valid_branches:
        return None

    latest_branch = max(valid_branches, key=version_key)

    return latest_branch
