## Jira MCP Server

This is a simple prototype of a Jira Server/DC MCP server.
It uses Python APIs for Jira documented [here](https://github.com/atlassian-api/atlassian-python-api), and the MCP Python SDK.

### Run steps
1. Copy .env.example to .env, and replace ```YOUR_JIRA_HOST_URL``` and ```YOUR_JIRA_PERSONAL_ACCESS_TOKEN```. The Jira host url must belong to a Jira server/ DC (the project is intended for Jira server/ DC). To generate your Personal Access Token, refer the section 'Creating PATs in the application' [here](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html).
2. Create and activate virtual environment, and install dependencies - ```pip install -r requirements.txt```
3. Run ```mcp dev mcp_server.py``` - this runs MCP Inspector which is a local way to test the defined tools and responses without involving an LLM.

### MCP Integration
The server can be started using ```python mcp_server.py```.

1. With Claude Desktop - Add to your claude_desktop_config.json the command and args :
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
Include the full paths of the python binary and the mcp_server.py file on your system ([reference](https://modelcontextprotocol.io/quickstart/user)).


2. With Other MCP Clients - The server follows the standard MCP protocol and works with any MCP-compatible client.

### Project Structure
```
JiraMCPserver/
├── jira_client/
│   ├── __init__.py
│   │── client.py
|   |── issue.py
|   └── project.py
├── models/
│   ├── __init__.py
│   │── constants.py
|   └── issue.py
├── mcp_server.py
├── .env.example
├── .gitignore
└── requirements.txt
```

### Supported operations -
This currently supports read-only issue and project management tools, for example
- "Give me all issues which are related to Recovery and open for more than 90 days"
- "List all issues assigned to Harshal Mittal resolved in last 30 days"
- "Find count of all open issues in ENG project"


Tools for write/ updating Jira can be added in similar way.
