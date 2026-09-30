# Connect your assistant

Start at [Connect Tross MCP](https://app.ontross.com/mcp/connect). Choose your client, then **Copy URL & open**.

## ChatGPT

1. Open [ChatGPT Plugins](https://chatgpt.com/plugins) and select **+ → Create MCP App**.
2. Enter **Tross MCP**, paste `https://mcp.ontross.com/mcp` and choose **OAuth**.
3. Create the app, connect it and sign in to Tross.
4. Select **Try in chat** and ask **“List my Tross connections.”**

If app creation is unavailable, check **Settings → Security and login → Developer mode**. Workspace policy may require an administrator. See [OpenAI's setup guide](https://developers.openai.com/plugins/deploy/connect-chatgpt).

## Claude

1. Open [Claude Connectors](https://claude.ai/customize/connectors) and choose **Add custom connector**.
2. Enter **Tross MCP** and `https://mcp.ontross.com/mcp`.
3. Connect and sign in to Tross.
4. Enable Tross in a new chat and ask **“List my Tross connections.”**

Claude may also ask permission to use a tool. This is separate from approving a write in Tross.

## Claude Code

```sh
claude mcp add --transport http tross https://mcp.ontross.com/mcp
claude mcp login tross
```

Complete sign-in in your browser, then ask Claude Code to list your Tross connections.

## Choose your access

Open the connection link returned by Tross. Choose your organization, connection and permitted operations, then return to your assistant.

To change an existing assistant's permissions, open [Connections](https://app.ontross.com/mcp/settings) and select **Edit access**. An organization administrator saves the selection; then ask the assistant to list connections again. Adding write access still requires human approval for each proposed change.

For an account-free demo, use `https://mcp.ontross.com/sandbox/mcp` and choose **No authentication** in ChatGPT or **No sign-in** in Claude. In Claude Code, add that URL instead of the production URL; no login is needed. Keep the `sandbox_session` returned by Tross on follow-up tool calls so changes and files remain available.

## Troubleshooting

- **No connections:** open the returned Tross connection link and check your organization and permissions.
- **Operation not permitted:** ask your administrator to enable it through **Connections → Edit access**, then list connections again. If the OAuth scope is missing, reconnect the assistant with the required permissions.
- **Authentication error:** reconnect using the exact server URL above. Production uses OAuth; an ordinary API key cannot authenticate this MCP connection.
- **Missing tools:** reconnect or refresh the server in your client.
- **Write awaiting approval:** open its review link in Tross, then return to your assistant to retrieve the result.
