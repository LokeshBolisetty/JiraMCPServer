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
        issue = self.jira.issue(key)

        # Filter out null fields recursively if issue is a dictionary
        if isinstance(issue, dict):
            return self._remove_null_values(issue)
        return issue

    def GetIssueComments(self, issue_id_or_key: str):
        """Get comments for a single issue."""
        return self.jira.issue_get_comments(issue_id_or_key)

    def GetIssues(self, jql: str):
        """Get Issues filtered using JQL"""
        issues = self.jira.jql(jql)
        return self._getFilteredIssues(issues)

    def GetLinkedIssues(self, issue_key: str, relationship_type: str = None):
        """Get issues linked to the specified issue.

        Args:
            issue_key: The Jira issue key
            relationship_type: Optional type of relationship. If None, all linked issues are returned.

        Returns:
            List of linked issues with their relationship types
        """
        # Get the issue with links
        issue = self.jira.issue(issue_key, fields="issuelinks")
        linked_issues = []

        if "fields" not in issue or "issuelinks" not in issue["fields"]:
            return []

        for link in issue["fields"]["issuelinks"]:
            # Determine the relationship type and target issue
            if "outwardIssue" in link:
                # This issue is the source of the link
                link_type = link.get("type", {}).get("outward", "relates to")
                target_issue_key = link["outwardIssue"]["key"]
                target_issue = link["outwardIssue"]
            elif "inwardIssue" in link:
                # This issue is the target of the link
                link_type = link.get("type", {}).get("inward", "relates to")
                target_issue_key = link["inwardIssue"]["key"]
                target_issue = link["inwardIssue"]
            else:
                continue

            # Filter by relationship type if specified
            if relationship_type and relationship_type.lower() != link_type.lower():
                continue

            # Add to results
            linked_issues.append({
                "key": target_issue_key,
                "relationship": link_type,
                "summary": target_issue.get("fields", {}).get("summary", "")
            })

        return linked_issues

    def SearchIssuesByText(self, text: str, max_results: int = 10):
        """Search for Jira issues containing specific text in title, description, or comments.

        Args:
            text: The text to search for
            max_results: Maximum number of issues to return

        Returns:
            List of matching JiraIssue objects
        """
        # Clean and escape the text for JQL
        # Remove quotes and special chars that could break JQL
        clean_text = text.replace('"', ' ').replace('~', ' ').replace('\\', ' ')

        # Create JQL to search in multiple fields including comments
        jql = f'text ~ "{clean_text}" OR summary ~ "{clean_text}" OR description ~ "{clean_text}" OR comment ~ "{clean_text}"'

        # Execute the search
        issues = self.jira.jql(jql, limit=max_results)
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

    # Helper function.
    def _remove_null_values(self, obj):
        """Recursively remove null values from dictionaries and lists."""
        if isinstance(obj, dict):
            return {k: self._remove_null_values(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [self._remove_null_values(item) for item in obj if item is not None]
        else:
            return obj

