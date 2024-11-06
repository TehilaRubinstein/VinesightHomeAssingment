import httpx
from fastapi import FastAPI, HTTPException
from typing import List
from models import RepositoryRevisions, RevisionsDiff
from github_service import get_commit_diff
import asyncio

from logging_setup import setup_logging

# Initialize the logger
logger = setup_logging()

app = FastAPI()


@app.post("/diff", response_model=List[RevisionsDiff])
async def get_revisions_diff(repos: List[RepositoryRevisions]):
    """
    Retrieves the differences in commits be tween two revisions for multiple repositories.

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
    logger.info("Received request to get revisions diff for %d repositories", len(repos))
    tasks = [
        get_commit_diff(repo.repository, repo.revisions[0], repo.revisions[1], repo.github_api_key)
        for repo in repos
    ]
    try:
        results = await asyncio.gather(*tasks)
        response_data = [
            RevisionsDiff(repository=repo.repository, revisions_diff=result)
            for repo, result in zip(repos, results)
        ]
        logger.debug("Revisions diff result: %s", response_data)
        return response_data
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.error(f"Not found: {e.request.url}")
            raise HTTPException(status_code=404, detail="Not found.")
        else:
            logger.error("HTTP error while fetching commits: %s", e)
            raise HTTPException(status_code=400, detail=f"Error fetching commits: {str(e)}")
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


