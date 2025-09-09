using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

using Microsoft.Extensions.Configuration;

IConfiguration configuration = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables()
    .AddCommandLine(args)
    .Build();

static (string? azoaEndpoint, string? azoaApiKey, string? aoaiModelId, string? azoaDeployedModel) GetConfig(IConfiguration config)
{
    var azoaEndpoint = config["azoaEndpoint"];
    var azoaApikey = config["azoaApiKey"];
    var azoaModelId = config["azoaModelId"];
    var azoaDeployedModel = config["azoaDeployedModel"];
    return (azoaEndpoint, azoaApikey, azoaModelId, azoaDeployedModel);
}

Console.WriteLine("C# MCP client to talk to Azure MCP server ");
var (azoaEndpoint, azoaApikey, azoaModel, azoaDeployedModel) = GetConfig(configuration);

IChatClient client =
    new ChatClientBuilder(
        new AzureOpenAIClient(new Uri(azoaEndpoint),
        new DefaultAzureCredential())
        .GetChatClient("gpt-4o").AsIChatClient())
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

Console.WriteLine($"There are a total of {availableTools.Count} Azure tools");
foreach (var tool in availableTools)
{
    Console.WriteLine($"Tool name: {tool.Name}");
}

List<ChatMessage> messages = [];

while (true)
{
    Console.WriteLine("Prompt(e to exit):");

    var input = Console.ReadLine();

    if (input == "e") break;

    messages.Add(new(ChatRole.User, input));

    // Get responses from LLM
    List<ChatResponseUpdate> llmResponses = [];
    await foreach (var response in client.GetStreamingResponseAsync(messages, new() { Tools = [.. availableTools] }))
    {
        // print response
        Console.Write(response);
        // add to list of chat messages
        llmResponses.Add(response);
    }
    Console.WriteLine();
    messages.AddMessages(llmResponses);
}
Console.WriteLine("Thankyou for using Azure MCP server chat!");
