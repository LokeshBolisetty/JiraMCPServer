import json
from .client import Jira
from models import DEFAULT_READ_JIRA_FIELDS

class ManageIssues:
    """Class for managing Jira issues."""

    def __init__(self, jira_client: Jira):
        self.jira = jira_client
    
    def GetIssuesForBoard(
            self,
            board_id: str,
            jql: str = "",
            fields: str | None = None,
            start: int = 0,
            limit: int = 50) -> str:
        """Get issues for a specific board."""
        fields_param = fields or ",".join(DEFAULT_READ_JIRA_FIELDS)
        issues = self.jira.get_issues_for_board(board_id=board_id, jql=jql,
                            fields=fields_param, start=start, limit=limit)
        return json.dumps(issues, indent=4)
    
    def GetIssuesForProject(self, project_key: str, fields: str | None = None, start: int = 0, limit: int = 50) -> str:
        """Get issues for a specific project."""
        fields_param = fields or ",".join(DEFAULT_READ_JIRA_FIELDS)
        issues = self.jira.get_all_project_issues(project_key, fields=fields_param, start=start, limit=limit)
        return json.dumps(issues, indent=4)

    def GetIssue(self, key: str):
        """Get a single issue by key."""
        return self.jira.issue(key)
    
    def GetIssueComments(self, issue_id_or_key: str):
        """Get comments for a single issue."""
        return self.jira.issue_get_comments(issue_id_or_key)
    
    def GetIssues(self, jql: str):
        """Get Issues filtered using JQL"""
        issues = self.jira.jql(jql)
        return self._getFilteredIssues(issues)
    
    def _getFilteredIssues(self, issues):
        """FIlter issues to include only important fields"""
        filtered_issues = []

        for issue in issues.get('issues', []):
            filtered_issue = {
                'key': issue.get('key'),
                'summary': issue.get('fields', {}).get('summary'),
                'status': issue.get('fields', {}).get('status', {}).get('name'),
            }
            filtered_issues.append(filtered_issue)

        return json.dumps(filtered_issues, indent=4)
        
