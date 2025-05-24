from mcp.server.fastmcp import FastMCP
from jira_client import JiraClient, ManageIssues, ManageProjects
from models import JiraIssue
from typing import List, Dict

# Instantiate the MCP server
mcp = FastMCP("Jira")

# Instantiate Jira management classes
jira_client = JiraClient().client
manage_projects = ManageProjects(jira_client)
manage_issues = ManageIssues(jira_client)

# Example tool

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# Issue Management Tools

@mcp.tool()
def get_issues_for_board(board_id: str, jql: str = "", limit: int = 20) -> List[JiraIssue]:
    """
    Retrieve issues from a specific Jira board.
    Args:
        board_id: The ID of the Jira board.
        jql: JQL query string to filter issues.
        limit: Maximum number of issues to return.
    Returns:
        List of JiraIssue objects.
    """
    return manage_issues.GetIssuesForBoard(board_id, jql, limit)

@mcp.tool()
def get_issues_for_project(project_key: str, limit: int = 20) -> List[JiraIssue]:
    """
    Retrieve issues from a specific Jira project.
    Args:
        project_key: The key or name of the Jira project.
        limit: Maximum number of issues to return.
    Returns:
        List of JiraIssue objects.
    """
    return manage_issues.GetIssuesForProject(project_key, limit)

@mcp.tool()
def get_issues(jql: str) -> List[JiraIssue]:
    """
    Filters and returns issues using JQL.
    Args:
        key: The JQL to use to filter issues.
    Returns:
        List of JiraIssue objects.
    """
    return manage_issues.GetIssues(jql)

@mcp.tool()
def get_issue(key: str) -> JiraIssue:
    """
    Retrieve details of a specific Jira issue.
    Args:
        key: The Jira issue key.
    Returns:
        JiraIssue object.
    """
    return manage_issues.GetIssue(key)

@mcp.tool()
def get_issue_comments(issue_id_or_key: str) -> List[Dict]:
    """
    Retrieve comments for a specific Jira issue.
    Args:
        issue_id_or_key: The Jira issue key or ID.
    Returns:
        List of comment dictionaries.
    """
    return manage_issues.GetIssueComments(issue_id_or_key)

# Project Management Tools

@mcp.tool()
def get_projects() -> List[Dict]:
    """
    Retrieve all Jira projects.
    Returns:
        List of project dictionaries.
    """
    return manage_projects.GetProjects()

@mcp.tool()
def get_project_count() -> int:
    """
    Retrieve the count of all active Jira projects.
    Returns:
        Integer count of projects.
    """
    return manage_projects.GetProjectsCount()

@mcp.tool()
def get_issues_count_for_project(project_key: str) -> int:
    """
    Retrieve the count of issues for a specific Jira project.
    Args:
        project_key: The key or name of the Jira project.
    Returns:
        Integer count of issues.
    """
    return manage_projects.GetIssueCountForProject(project_key)


if __name__ == "__main__":
    mcp.run()
