import httpx
from fastapi import FastAPI, HTTPException
from typing import List
from models import RepositoryRevisions, RevisionsDiff
from github_service import get_commit_diff
import asyncio

app = FastAPI()

@app.post("/diff", response_model=List[RevisionsDiff])
async def get_revisions_diff(repos: List[RepositoryRevisions]):
    """
    Retrieves the differences in commits between two revisions for multiple repositories.

    This endpoint accepts a list of repository revision objects and asynchronously fetches
    the commit differences for each specified revision in the repositories. The results
    are returned as a list of `RevisionsDiff` objects.

    Args:
        repos (List[RepositoryRevisions]): A list of objects containing repository names
                                             and their corresponding revisions to compare.

    Returns:
        List[RevisionsDiff]: A list of `RevisionsDiff` objects, each containing the repository name
                             and the differences in commits between the two specified revisions.

    Raises:
        HTTPException: If an error occurs while fetching commits from the GitHub API, a 400
                       HTTP error is raised with details of the issue.
    """
    tasks = [
        get_commit_diff(repo.repository, repo.revisions[0], repo.revisions[1], repo.github_api_key)
        for repo in repos
    ]
    try:
        results = await asyncio.gather(*tasks)
        return [
            RevisionsDiff(repository=repo.repository, revisions_diff=result)
            for repo, result in zip(repos, results)
        ]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Error fetching commits: {str(e)}")

