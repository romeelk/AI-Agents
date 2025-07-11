# Introduction

This repo project shows how to use the MCP Server for Azure by integrating it with
GitHub Copilot VSCode extension

# Pre-requisites

The following is required:

- An active Azure subscription
- GitHub Copilot 
- Visual Studio Code IDE

## Installing the VSCode extension

Create an empty .vscode in folder in your project directory. I suggest create a separate project to test this.

```
mkdir .vscode
```

## Create a mcp.json

Inside the new .vscode folder create the following mcp.json file:

```
{
  "servers": {
    "Azure MCP Server": {
      "command": "npx",
      "args": [
        "-y",
        "@azure/mcp@latest",
        "server",
        "start"
      ]
    }
  }
}

```

## Select Azure MCPServer

Ensure you are authenticated to your Azure sub. 

Select cmd-i to open GitHub Copiliot.

Select the tools icon as shown in the screenshoot.

Search for "Azure MCPServer" and select the tool.

## Query and create resource in your Azure sub

Type the following in the prompt:

```
List my Azure resource groups.

```

If it is successful it should query your Azure sub.

Now ask it to create a resource group:

```
Can you create a resource group called rg-mcpdemo?

```

Again if successful it should ask you to run a azure cli command (human in the loop)

And create the resource group.

![image](mcp-azure.png)


