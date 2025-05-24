import os
from dotenv import load_dotenv
from atlassian import Jira
# Loads variables from .env into the environment
load_dotenv() 

JIRA_URL = os.environ.get("JIRA_URL")
JIRA_PERSONAL_ACCESS_TOKEN = os.environ.get("JIRA_PERSONAL_ACCESS_TOKEN")

class JiraClient:
    def __init__(self):
        """Instantiate and return a Jira client."""
        self.client = Jira(
            url=JIRA_URL,
            token=JIRA_PERSONAL_ACCESS_TOKEN
        )

