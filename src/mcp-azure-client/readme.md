# Introduction

This demo shows how to connect to a MCP server to query about Azure information.

It uses Azure AI Foundry to create an AI agent that can use the mcp tool.

## Pre-requesites

1) latest Node version. Make sure you have a node version > v20
- on Mac run  nvm install node —lts
2) Access to azure subscription
3) VS Code installed


## Verify azure mcp server

You can verify the node package @azure/mcp@latest runs 

```
 npx -y @azure/mcp@latest server start
```