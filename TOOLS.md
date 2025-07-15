# Jira MCP Server Tools Documentation

This document provides detailed information about the tools available in the Jira MCP Server, including their purpose, parameters, and usage examples.

## Available MCP Tools

### Jira Issue Tools

#### 1. `get_issues(jql: str)`
- **Purpose**: Search for Jira issues using JQL (Jira Query Language)
- **Parameters**:
  - `jql`: A valid JQL query string
- **Returns**: List of issues matching the query
- **Example**:
  ```python
  get_issues('project = ENG AND status = "In Progress"')
  ```

#### 2. `get_issue(key: str)`
- **Purpose**: Get details of a specific Jira issue
- **Parameters**:
  - `key`: Jira issue key (e.g., "ENG-123")
- **Returns**: Complete issue details including fields, comments (if requested), and metadata
- **Example**:
  ```python
  get_issue("ENG-123")
  ```

#### 3. `get_issue_comments(issue_id_or_key: str)`
- **Purpose**: Get all comments for a specific Jira issue
- **Parameters**:
  - `issue_id_or_key`: Jira issue key or ID
- **Returns**: List of comments with author and content details
- **Example**:
  ```python
  get_issue_comments("ENG-123")
  ```

#### 4. `get_issues_for_board(board_id: str, jql: str = "", limit: int = 20)`
- **Purpose**: Get issues from a specific board with optional JQL filtering
- **Parameters**:
  - `board_id`: ID of the Jira board
  - `jql`: Optional JQL filter
  - `limit`: Maximum number of issues to return (default: 20)
- **Returns**: List of issues from the specified board
- **Example**:
  ```python
  get_issues_for_board("123", 'status = "In Progress"', 10)
  ```

#### 5. `get_issues_for_project(project_key: str, limit: int = 20)`
- **Purpose**: Get all issues in a specific project
- **Parameters**:
  - `project_key`: The Jira project key
  - `limit`: Maximum number of issues to return (default: 20)
- **Returns**: List of issues in the project
- **Example**:
  ```python
  get_issues_for_project("ENG", 15)
  ```

#### 6. `search_issues_by_text(text: str, max_results: int = 10)`
- **Purpose**: Search for issues containing specific text in title, description, or comments
- **Parameters**:
  - `text`: Text to search for (can be error message, stack trace, or any keyword)
  - `max_results`: Maximum number of results to return (default: 10)
- **Returns**: List of matching issues with key, summary, and status
- **Example**:
  ```python
  search_issues_by_text("NullPointerException", 5)
  ```

#### 7. `get_linked_issues(issue_key: str, relationship_type: str = None)`
- **Purpose**: Get issues linked to a specific issue
- **Parameters**:
  - `issue_key`: The Jira issue key (e.g., "ENG-123")
  - `relationship_type`: Optional relationship type filter (e.g., "blocks", "relates to")
- **Returns**: List of linked issues with their relationship types
- **Example**:
  ```python
  get_linked_issues("ENG-123", "blocks")
  ```

### Project Tools

#### 1. `get_projects()`
- **Purpose**: List all Jira projects
- **Returns**: List of project dictionaries with key, name, and metadata
- **Example**:
  ```python
  get_projects()
  ```

#### 2. `get_project_count()`
- **Purpose**: Get the total number of active Jira projects
- **Returns**: Integer count of projects
- **Example**:
  ```python
  get_project_count()
  ```

#### 3. `get_issues_count_for_project(project_key: str)`
- **Purpose**: Get the number of issues in a project
- **Parameters**:
  - `project_key`: The project key
- **Returns**: Integer count of issues
- **Example**:
  ```python
  get_issues_count_for_project("ENG")
  ```

### Other Tools

#### 1. `add(a: int, b: int)`
- **Purpose**: Simple addition tool for testing the MCP connection
- **Parameters**:
  - `a`: First integer
  - `b`: Second integer
- **Returns**: Sum of a and b
- **Example**:
  ```python
  add(2, 3)  # Returns 5
  ```

## Example Workflows

### Finding Issues with Error Messages
```python
# Find all issues with error messages
error_issues = search_issues_by_text("NullPointerException")

# For each issue, get linked issues to find related context
for issue in error_issues:
    linked = get_linked_issues(issue['key'])
    # Process linked issues...
```

### Analyzing Project Issues
```python
# Get all in-progress issues
issues = get_issues('project = ENG AND status = "In Progress"')

# Analyze each issue
for issue in issues:
    details = get_issue(issue['key'])
    comments = get_issue_comments(issue['key'])
    # Process issue details and comments...
```

### Finding Related Issues and Their Context
```python
# Find a specific issue
issue = get_issue("ENG-123")

# Get all related issues
related = get_linked_issues("ENG-123")

# Get comments for context
for rel_issue in related:
    comments = get_issue_comments(rel_issue['key'])
    # Analyze comments for relevant information...
```

## Best Practices
1. Always use specific JQL queries to limit the number of results
2. Use `max_results` parameter to prevent excessive data retrieval
3. Check for null values in responses (the server automatically filters these out)
4. Handle rate limiting (the server implements basic rate limiting)
5. For complex analyses, combine multiple tools to gather comprehensive context
6. When searching for error messages, consider cleaning the text to focus on the key parts of the error
