import pytest
import logging
from fastapi.testclient import TestClient
from main import app

# Initialize the test client for the FastAPI app
client = TestClient(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Expected commit SHAs that are unique to the first revision (rev1)
expected_commits_rev1 = {
    "3f822818b25c042280cbecce1968ca11006ba8e4",
    "3f3637ba73d0e15ce2d57910697aed7f152316f6",
    "46a085ebe7dd24129023a197f2eff6e9e8089afe",
    "6e07910cc4112bea61473fe8f69a272fdeb5e526",
    "8cae611101fb4b1e6804df032c020758447a7ded",
    "c8f5755d0a14f6013a3667f3414753cbe1604660",
    "268eac9e16cccf2b60bcc1d4a70ff3b15b6958b9",
    "25c63800f6c5c76b8514d6f3c3b3178c12e24471",
    "c5a9d3ac28cd21a010608f36c9967c7185a54904",
    "8dc523b1efda92d878796c22f9a4a88f4a03605a",
    "a9d9433514f1b9f50641898fb7b86ae2be023a3d"
}

# Expected commit SHAs that are unique to the second revision (rev2)
expected_commits_rev2 = {
    "e05a90b102664f68cb855122877466e9daa6918a",
    "304311268aa5ba93c31a2ca8a9fd289c67717dd0",
    "060a7920f43973cc4c1e96c3901083bd3e96f4f9"
}

# Revision identifiers for comparison in the test
rev1 = 'a9d9433514f1b9f50641898fb7b86ae2be023a3d'
rev2 = '060a7920f43973cc4c1e96c3901083bd3e96f4f9'


def test_get_revisions_diff():
    """
    Tests the '/diff' endpoint for retrieving the differences in commits between two revisions.

    This function sends a POST request with repository and revision data to the '/diff' endpoint
    and verifies that the response:
        - Returns a 200 status code
        - Contains the expected keys: 'repository' and 'revisions_diff'
        - Includes the expected unique commits for each revision (rev1 and rev2)

    Raises:
        AssertionError: If any of the response checks fail.
    """
    # Send a POST request to the '/diff' endpoint with repository and revision details
    logger.info("Starting test for '/diff' endpoint")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "fastapi/fastapi",
                "revisions": [
                    rev1,
                    rev2
                ]
            }
        ]
    )

    # Validate response status and structure
    assert response.status_code == 200, logger.error(f"Expected 200, got {response.status_code}")
    assert "repository" in response.json()[0], logger.error("Missing 'repository' in response")
    assert "revisions_diff" in response.json()[0], logger.error("Missing 'revisions_diff' in response")

    # Extract unique commits for each revision
    rev1_diff = response.json()[0]['revisions_diff'].get(rev1, [])
    rev2_diff = response.json()[0]['revisions_diff'].get(rev2, [])

    # Validate unique commits for each revision
    logger.info("Checking expected commits for rev1")
    assert expected_commits_rev1.issubset(rev1_diff), \
        logger.error(f"Expected commits for rev1 are not fully present in the response: {expected_commits_rev1 - set(rev1_diff)}")

    logger.info("Checking expected commits for rev2")
    assert expected_commits_rev2.issubset(rev2_diff), \
        logger.error(f"Expected commits for rev2 are not fully present in the response: {expected_commits_rev2 - set(rev2_diff)}")

    logger.info("Test '/diff' passed successfully")


def test_missing_method():
    """Test case where a request is sent to the /diff endpoint without using PUT or POST."""
    logger.info("Running test_missing_method")
    response = client.get("/diff")
    logger.info("Received response status code: %s", response.status_code)
    assert response.status_code == 405  # Method Not Allowed

def test_missing_body():
    """Test case where a POST request is sent to /diff without body."""
    logger.info("Running test_missing_body")
    response = client.post("/diff")
    logger.info("Received response status code: %s", response.status_code)
    assert response.status_code == 422  # Unprocessable Entity

def test_invalid_repository():
    """Test case where a non-existent repository or revision is provided."""
    logger.info("Running test_invalid_repository_revision")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "nonexistent_user/nonexistent_repo",
                "revisions": [
                    rev1,
                    rev2
                ]
            }
        ]
    )
    logger.info("Received response: %s", response.json())
    assert response.status_code == 404
    assert "Not found" in response.json()["detail"]
def test_invalid_revisions():
    """Test case where a non-existent repository or revision is provided."""
    logger.info("Running test_invalid_repository_revision")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "fastapi/fastapi",
                "revisions": [
                    "fake_revision_1",
                    "fake_revision_2"
                ]
            }
        ]
    )
    logger.info("Received response: %s", response.json())
    assert response.status_code == 404
    assert "Not found" in response.json()["detail"]

def test_more_than_two_revisions():
    """Test case where more than two revisions are provided."""
    logger.info("Running test_more_than_two_revisions")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "fastapi/fastapi",
                "revisions": [
                    "main",
                    "dev",
                    "feature-branch"
                ]
            }
        ]
    )
    logger.info("Received response status code: %s", response.status_code)
    assert response.status_code == 422  # Unprocessable Entity

def test_less_than_two_revisions():
    """Test case where only one revision is provided."""
    logger.info("Running test_less_than_two_revisions")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "fastapi/fastapi",
                "revisions": [
                    "main"
                ]
            }
        ]
    )
    logger.info("Received response status code: %s", response.status_code)
    assert response.status_code == 422  # Unprocessable Entity

def test_request_without_token():
    """Test case where a valid request is sent without a GitHub token."""
    logger.info("Running test_request_without_token")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "fastapi/fastapi",
                "revisions": [
                    rev1,
                    rev2
                ]
            }
        ]
    )
    logger.info("Received response: %s", response.json())
    assert response.status_code == 200
    logger.info("Test completed successfully.")

def test_private_repo_without_token():
    """
    Test case where a request is sent to access a private repository without providing a token.

    This should return a 401 Unauthorized error because the GitHub API requires
    authentication to access private repositories.
    """
    logger.info("Running test_private_repo_without_token")
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "yairogen/dummy",
                "revisions": [
                    "bd11eae80aa668b24d2b5b63efcce694c18cd7a5",
                    "72944becb519753a7138034933e3f9daa1fb6387"
                ]
            }
        ]
    )
    logger.info("Received response status code: %s", response.status_code)
    logger.info("Response content: %s", response.json())
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "Not found" in response.json()["detail"]


