using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;
Console.WriteLine("C# MCP client to talk to Azure MCP server ");

IChatClient client =
    new ChatClientBuilder(
        new AzureOpenAIClient(new Uri("https://sk-agent-demo-rk.cognitiveservices.azure.com/>"),
        new DefaultAzureCredential())
        .GetChatClient("gpt-40").AsIChatClient())
        .UseFunctionInvocation()
        .Build();

// Create MCP Client to Azure
// Create the MCP client
var mcpClient = await McpClientFactory.CreateAsync(
    new StdioClientTransport(new()
    {
        Command = "npx",
        Arguments = ["-y", "@azure/mcp@latest", "server", "start"],
        Name = "Azure MCP",
    }));

// list the mcp tools

var availableTools = await mcpClient.ListToolsAsync();

foreach (var tool in availableTools)
{
    Console.WriteLine($"Tool name: {tool.Name}, Deccription: {tool.Description}");
}

