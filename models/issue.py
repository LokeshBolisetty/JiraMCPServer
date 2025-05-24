from pydantic import BaseModel
from .constants import UNASSIGNED, UNKNOWN, EMPTY_STRING, JIRA_DEFAULT_ID, NONE_VALUE

class JiraUser(BaseModel):
    """
    Model representing a Jira user.
    """

    account_id: str | None = None
    display_name: str = UNASSIGNED
    email: str | None = None
    active: bool = True
    avatar_url: str | None = None
    time_zone: str | None = None

class JiraStatusCategory(BaseModel):
    """
    Model representing a Jira status category.
    """

    id: int = 0
    key: str = EMPTY_STRING
    name: str = UNKNOWN
    color_name: str = EMPTY_STRING

class JiraStatus(BaseModel):
    """
    Model representing a Jira issue status.
    """

    id: str = JIRA_DEFAULT_ID
    name: str = UNKNOWN
    description: str | None = None
    icon_url: str | None = None
    category: JiraStatusCategory | None = None

class JiraIssueType(BaseModel):
    """
    Model representing a Jira issue type.
    """

    id: str = JIRA_DEFAULT_ID
    name: str = UNKNOWN
    description: str | None = None
    icon_url: str | None = None

class JiraPriority(BaseModel):
    """
    Model representing a Jira priority.
    """

    id: str = JIRA_DEFAULT_ID
    name: str = NONE_VALUE
    description: str | None = None
    icon_url: str | None = None

class JiraIssue(BaseModel):
    summary: str = EMPTY_STRING
    status: JiraStatus | None = None
    assignee: JiraUser | None = None
    reporter: JiraUser | None = None
    created: str = EMPTY_STRING
    updated: str = EMPTY_STRING
    issue_type: JiraIssueType | None = None
    priority: JiraPriority | None = None
    url: str | None = None