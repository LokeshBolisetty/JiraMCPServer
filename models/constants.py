DEFAULT_READ_JIRA_FIELDS: set[str] = {
    "summary",
    "description",
    "status",
    "assignee",
    "reporter",
    "labels",
    "priority",
    "created",
    "updated",
    "issuetype",
}

JIRA_DEFAULT_ID = "0"
UNKNOWN = "Unknown"
UNASSIGNED = "Unassigned"
NONE_VALUE = "None"
EMPTY_STRING = ""