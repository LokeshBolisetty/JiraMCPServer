from .client import Jira

class ManageProjects:
    """Class for managing Jira projects."""

    def __init__(self, jira_client: Jira):
        self.jira = jira_client

    def GetProjects(self):
        """Get all projects."""
        return self.jira.projects(included_archived=None, expand=None)

    def GetProjectsCount(self) -> int:
        """Get the count of all projects."""
        projects = self.jira.projects(included_archived=None, expand=None)
        return len(projects)
    
    def GetIssueCountForProject(self, project_key: str) -> int:
        """Get the count of issues for a specific project."""
        try:
            # Use JQL to count issues in the project
            jql = f"project = {project_key}"
            result = self.jira.jql(jql=jql, fields="key", limit=1)
            if not isinstance(result, dict):
                msg = f"Unexpected return value type from `jira.jql`: {type(result)}"
                raise TypeError(msg)

            # Extract total from the response
            total = 0
            if isinstance(result, dict) and "total" in result:
                total = result.get("total", 0)

            return total

        except Exception as e:
            raise Exception