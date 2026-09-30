# Tross MCP

Connect your healthcare AI to EHR and payer workflows.

**[Connect Tross MCP](https://app.ontross.com/mcp/connect)** · [Explore capabilities](https://app.ontross.com/mcp/catalog) · [Watch demos](https://app.ontross.com/mcp#watch)

Use Tross from ChatGPT, Claude or your own agent to retrieve healthcare data and complete approved actions. Every external write requires a person to review and approve it in Tross. MCP is included in existing Tross commercial terms.

## Connect

1. Open [Connect Tross MCP](https://app.ontross.com/mcp/connect) and choose your client.
2. Add the server and sign in to Tross.
3. Select your connection and the operations your assistant can use.

Production server: `https://mcp.ontross.com/mcp`

[Setup instructions](docs/connect.md) cover ChatGPT, Claude and Claude Code. Need a Tross connection? [Request access](https://app.ontross.com/mcp/request-access).

## Try it without an account

[Connect to the sandbox](https://app.ontross.com/mcp/connect?mode=sandbox) to explore the same approval flow with isolated demo records.

```sh
git clone https://github.com/getayden/tross-mcp.git
cd tross-mcp
python -m pip install 'mcp>=1.30,<2' httpx
python examples/tross-mcp/client.py --operation ecw/fetch-notes --connection demo-ecw --input examples/tross-mcp/inputs/read-notes.json
```

The [Python example](examples/tross-mcp/README.md) also covers write proposals, polling and attachments.

## Explore

- [Client setup](docs/connect.md)
- [Workflow examples](docs/workflows.md)
- [Permissions, approvals and files](docs/permissions.md)
- [Demo videos](docs/demos.md)

Available workflows depend on your connection and permissions. Use the [capability directory](https://app.ontross.com/mcp/catalog) or ask your assistant to find a Tross operation.
