# GitHub Revision Diff Service

## Overview

This FastAPI service provides an endpoint (`/diff`) that compares two revisions (branches or commits) within a GitHub repository, returning unique commits in each revision. 

## Installation

1. Clone the repository.
2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage
Running the Application:

```bash
uvicorn main:app --reload
```
## Testing
Run the tests with:
```bash
pytest test_main.py
```


## API Endpoints
POST /diff
Description: Compares two revisions in a GitHub repository and returns unique commits in each.

Request Body:
* repository: Repository name (e.g., owner/repo).
* revisions: List of two revisions (e.g., ["main", "dev"]).
* github_api_key (optional): GitHub access token.
Response:
List of objects with repository and revisions_diff (unique commits in each revision).

### Request Body Example

The request body should include the following structure:
first option - without token (public repository):

```json
[
  {
    "repository": "owner/repo",
    "revisions": ["revision1", "revision2"]
  }
]
```

second option - with token (private repository):
```json
[
   {
    "repository": "yairogen/dummy",
    "revisions": [
                "bd11eae80aa668b24d2b5b63efcce694c18cd7a5",
                "72944becb519753a7138034933e3f9daa1fb6387"
        ],
        "github_api_key":"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"
    }
]
```
#### Example Request
To make a request to the /diff endpoint, you can use curl or an HTTP client like httpx. Below is an example using curl:

first option:
```bash
curl -X POST "http://127.0.0.1:8000/diff" -H "Content-Type: application/json" -d '[
  {
    "repository": "fastapi/fastapi",
    "revisions": ["a9d9433514f1b9f50641898fb7b86ae2be023a3d", "060a7920f43973cc4c1e96c3901083bd3e96f4f9"]
  }
]'
```
second option:
```bash
curl -X POST curl -X POST "http://127.0.0.1:8000/diff" -H "Content-Type: application/json" -d '[
  {
    "repository": "yairogen/dummy",
    "revisions": [
                "bd11eae80aa668b24d2b5b63efcce694c18cd7a5",
                "72944becb519753a7138034933e3f9daa1fb6387"
        ],
        "github_api_key":"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"
    }
]'
```
#### Response Example
The response will contain a list of repositories with unique commit SHAs for each revision:

first option:
```json
[{
        "repository": "fastapi/fastapi",
        "revisions_diff": {
            "a9d9433514f1b9f50641898fb7b86ae2be023a3d": [
                "a9d9433514f1b9f50641898fb7b86ae2be023a3d",
                "8dc523b1efda92d878796c22f9a4a88f4a03605a",
                "c5a9d3ac28cd21a010608f36c9967c7185a54904",
                "25c63800f6c5c76b8514d6f3c3b3178c12e24471",
                "268eac9e16cccf2b60bcc1d4a70ff3b15b6958b9",
                "c8f5755d0a14f6013a3667f3414753cbe1604660",
                "8cae611101fb4b1e6804df032c020758447a7ded",
                "6e07910cc4112bea61473fe8f69a272fdeb5e526",
                "46a085ebe7dd24129023a197f2eff6e9e8089afe",
                "3f3637ba73d0e15ce2d57910697aed7f152316f6",
                "3f822818b25c042280cbecce1968ca11006ba8e4"
            ],
            "060a7920f43973cc4c1e96c3901083bd3e96f4f9": [
                "060a7920f43973cc4c1e96c3901083bd3e96f4f9",
                "304311268aa5ba93c31a2ca8a9fd289c67717dd0",
                "e05a90b102664f68cb855122877466e9daa6918a",
                "fe3922311f255a7ae0092c21e5c916b8d5ad0081",
                "96c5566a5b31422965e0e1b383ef0128b0acde7c",
                "218d3c352429674d18dad0a42747dcbcbb9fb36a",
                "0279f6dd5fc5613308d4dabd5af477a3ac8d42e9",
                "269a22454443c6d977f702fb41d3d40cff149123",
                "adf89d1d9fdc8ea03bc0f3361b3d5e4b6835cf6c",
                "96a6d469e917076749b36603f509a8adc39a050c",
                "dbc3008f5a3418271c31e7e3fe1051a7649f7289"
            ]
        }
    }]
```

second option:
```json
[
    {
        "repository": "yairogen/dummy",
        "revisions_diff": {
            "bd11eae80aa668b24d2b5b63efcce694c18cd7a5": [
                "bd11eae80aa668b24d2b5b63efcce694c18cd7a5"
            ],
            "72944becb519753a7138034933e3f9daa1fb6387": []
        }
    }
]
```

## Logging Configuration

This project uses a centralized logging configuration to capture log data from all modules and output it to a file (`app.log`) and the console. 

### Logging Setup
1. **Configuration**: The logging setup is defined in `logging_config.py`.
    - Logs are formatted to include timestamps, log levels, and module names.
    - Both `app.log` and the console will display logs for ease of debugging.
2. **Log Levels**: By default, the log level is set to `DEBUG` to capture detailed logs.
3. **Usage**:
   - Import the logger as `logger = logging.getLogger(__name__)` in any module.
   - Use `logger.info()`, `logger.debug()`, `logger.error()`, etc., to log messages.

### Example Logs
To view logs, open the `app.log` file. Here are some examples:
- `INFO` logs when endpoints are called or when certain operations succeed.
- `ERROR` logs for exceptions during API calls or data processing failures.

### Modifying the Log File Path
By default, logs are saved to `app.log` in the root directory. You can change this by modifying the path in `setup_logging()` in `logging_config.py`.

