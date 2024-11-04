import pytest
from fastapi.testclient import TestClient
from main import app

# Initialize the test client for the FastAPI app
client = TestClient(app)

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
    response = client.post(
        "/diff",
        json=[
            {
                "repository": "fastapi/fastapi",
                "revisions": [
                    "a9d9433514f1b9f50641898fb7b86ae2be023a3d",
                    "060a7920f43973cc4c1e96c3901083bd3e96f4f9"
                ]
            }
        ]
    )

    # Validate response status and structure
    assert response.status_code == 200
    assert "repository" in response.json()[0]
    assert "revisions_diff" in response.json()[0]

    # Verify that the expected unique commits are in the response for each revision
    assert expected_commits_rev1.issubset(
        response.json()[0]['revisions_diff'][rev1])
    assert expected_commits_rev2.issubset(
        response.json()[0]['revisions_diff'][rev2])
