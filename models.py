from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class RepositoryRevisions(BaseModel):
    """
    Model representing a GitHub repository and its revisions for comparison.

    Attributes:
        repository (str): The name of the repository in the format 'owner/repo'.
        revisions (List[str]): A list containing exactly two revision identifiers (branches or commit SHAs)
                               to compare. Must have a length of 2.
        github_api_key (Optional[str]): An optional personal access token for GitHub API authentication.
                                         If not provided, requests will be unauthenticated.
    """
    repository: str
    revisions: List[str] = Field(..., min_length=2, max_length=2)
    github_api_key: Optional[str] = None


class RevisionsDiff(BaseModel):
    """
    Model representing the differences in commits between two revisions of a GitHub repository.

    Attributes:
        repository (str): The name of the repository.
        revisions_diff (Dict[str, List[str]]): A dictionary where the keys are the revision identifiers
                                                and the values are lists of commit SHAs that are unique
                                                to each revision.
    """
    repository: str
    revisions_diff: Dict[str, List[str]]



