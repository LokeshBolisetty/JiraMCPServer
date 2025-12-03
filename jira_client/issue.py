import json
from .client import Jira
from models import DEFAULT_READ_JIRA_FIELDS
from typing import Dict, Any, Optional

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

    def AddComment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a Jira issue.

        Args:
            issue_key: The Jira issue key
            comment: The comment text to add

        Returns:
            Dictionary with the created comment data
        """
        try:
            result = self.jira.issue_add_comment(issue_key, comment)
            return result if result else {'success': True}
        except Exception as e:
            return {'error': str(e)}

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

    def CreateIssue(self, project_key: str, issue_type: str, summary: str, description: str = None,
                priority: str = None, labels: list = None, assignee: str = None,
                additional_fields: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new Jira issue.

        Args:
            project_key: The project key where the issue will be created
            issue_type: Type of the issue (e.g., 'Bug', 'Task', 'Story')
            summary: Issue summary/title
            description: Issue description
            priority: Priority of the issue (e.g., 'High', 'Medium', 'Low')
            labels: List of labels to attach to the issue
            assignee: Username of the assignee
            additional_fields: Additional fields to set on the issue

        Returns:
            Dictionary with the created issue data
        """
        # Build the issue fields
        issue_dict = {
            'project': {'key': project_key},
            'issuetype': {'name': issue_type},
            'summary': summary
        }

        # Add optional fields if provided
        if description:
            issue_dict['description'] = description

        if priority:
            issue_dict['priority'] = {'name': priority}

        if labels:
            issue_dict['labels'] = labels

        if assignee:
            issue_dict['assignee'] = {'name': assignee}

        # Add any additional fields
        if additional_fields:
            issue_dict.update(additional_fields)

        try:
            # Create the issue
            new_issue = self.jira.create_issue(fields=issue_dict)
            return self._remove_null_values(new_issue)
        except Exception as e:
            # Return error information
            return {'error': str(e)}

    def UpdateIssue(self, issue_key: str, summary: str = None, description: str = None,
                   priority: str = None, labels: list = None, assignee: str = None,
                   status: str = None, additional_fields: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update an existing Jira issue.

        Args:
            issue_key: The Jira issue key to update
            summary: New summary/title
            description: New description
            priority: New priority
            labels: New list of labels
            assignee: New assignee username
            status: New status/transition
            additional_fields: Additional fields to update

        Returns:
            Dictionary with the updated issue data
        """
        # Build the update fields
        issue_dict = {}

        if summary:
            issue_dict['summary'] = summary

        if description:
            issue_dict['description'] = description

        if priority:
            issue_dict['priority'] = {'name': priority}

        if labels:
            issue_dict['labels'] = labels

        if assignee:
            issue_dict['assignee'] = {'name': assignee}

        # Add any additional fields
        if additional_fields:
            issue_dict.update(additional_fields)

        try:
            # Update the issue
            if issue_dict:  # Only update if there are fields to update
                self.jira.update_issue_field(key=issue_key, fields=issue_dict)

            # Handle status transition if provided
            if status:
                # Get available transitions
                transitions = self.jira.get_issue_transitions(issue_key)
                transition_id = None

                # Find the transition ID for the requested status
                for transition in transitions:
                    if transition['name'].lower() == status.lower():
                        transition_id = transition['id']
                        break

                if transition_id:
                    self.jira.issue_transition(issue_key, transition_id)
                else:
                    return {'error': f'Status transition to "{status}" not available for this issue'}

            # Return the updated issue
            updated_issue = self.jira.issue(issue_key)
            return self._remove_null_values(updated_issue)
        except Exception as e:
            # Return error information
            return {'error': str(e)}

    # Helper function.
    def _remove_null_values(self, obj):
        """Recursively remove null values from dictionaries and lists."""
        if isinstance(obj, dict):
            return {k: self._remove_null_values(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [self._remove_null_values(item) for item in obj if item is not None]
        else:
            return obj

