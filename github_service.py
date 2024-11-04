import httpx
from typing import List, Dict, Optional

GITHUB_API_URL = "https://api.github.com"


async def fetch_commits(repo: str, revision: str, token: Optional[str] = None) -> List[str]:
    """
    Fetches the commit SHAs for a given repository and revision from the GitHub API.

    Args:
        repo (str): The owner and repository name in the format 'owner/repo'.
        revision (str): The branch or commit SHA to fetch commits from.
        token (Optional[str]): A personal access token for GitHub API authentication.
                               If not provided, the request will be unauthenticated.

    Returns:
        List[str]: A list of commit SHAs for the specified repository and revision.

    Raises:
        httpx.HTTPStatusError: If the HTTP request returned an unsuccessful status code.
    """
    headers = {"Authorization": f"token {token}"} if token else {}
    async with httpx.AsyncClient() as client:
        url = f"{GITHUB_API_URL}/repos/{repo}/commits?sha={revision}"
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return [commit["sha"] for commit in response.json()]

async def get_commit_diff(repo: str, rev1: str, rev2: str, token: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Compares two revisions of a repository and returns the commits that are unique to each revision.

    Args:
        repo (str): The owner and repository name in the format 'owner/repo'.
        rev1 (str): The first revision (branch or commit SHA) to compare.
        rev2 (str): The second revision (branch or commit SHA) to compare.
        token (Optional[str]): A personal access token for GitHub API authentication.
                               If not provided, the request will be unauthenticated.

    Returns:
        Dict[str, List[str]]: A dictionary with the unique commit SHAs for each revision,
                               where the keys are the revision identifiers.

    Raises:
        httpx.HTTPStatusError: If the HTTP request returned an unsuccessful status code.
    """
    commits_rev1 = await fetch_commits(repo, rev1, token)
    commits_rev2 = await fetch_commits(repo, rev2, token)

    return {
        rev1: list(filter(lambda x: x not in commits_rev2, commits_rev1)),
        rev2: list(filter(lambda x: x not in commits_rev1, commits_rev2))
    }
