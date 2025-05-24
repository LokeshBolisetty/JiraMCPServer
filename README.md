Jira MCP Server

This is a simple prototype of a Jira Server/DC MCP server.
It uses Python APIs for Jira documented at https://atlassian-python-api.readthedocs.io/, and MCP Python SDK.

To run it locally -
1. Copy .env.example to .env, and replace YOUR_JIRA_HOST_URL and YOUR_JIRA_PERSONAL_ACCESS_TOKEN. The Jira Host Url must be a server/ DC Jira url (the project is only tested with Jira server/ DC). For Personal Access Token generation, Refer https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html.
2. Create and activate virtual environment, and install dependencies - ```pip install -r requirements.txt```
3. Run ```mcp dev mcp_server.py``` to run MCP Inspector, that allows a local way for testing the defined tools and responses without using an LLM.
4. The server can be started as ```python mcp_server.py```.
5. To register and use MCP Server with any LLM, for example Claude Desktop Application, add it to the claude_desktop_config.json file (located at ~/Library/Application Support/Claude/claude_desktop_config.json on MacOS), which looks something like - 
```
{
  "mcpServers": {
    "jira": {
      "command": "/Users/harshal.mittal/.pyenv/versions/3.10.0/bin/python",
      "args": [
        "/Users/harshal.mittal/projects/jira-mcp-server/mcp_server.py"
      ]
    }
  }
}
```
Include the full paths of the python binary and the mcp_server.py file. (Reference - https://modelcontextprotocol.io/quickstart/user)
6. We can now ask any questions or control jira management using natural language.

Supported operations -
This currently supports issue and project management operations that are read only, for example
- "Give me all issues in project FI which are related to Recovery and open for more than 90 days"
- "List all issues assigned to Harshal Mittal resolved in last 30 days"
- "Find count of all issues in ENG project"
Write operations can be added easily as well if needed.
