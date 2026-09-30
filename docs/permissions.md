# Permissions, approvals and files

## Your connections

You choose which Tross connections and operations an assistant can use. Available workflows also depend on your provider and existing account permissions. Provider credentials stay with Tross.

Review access in [Connections & access](https://app.ontross.com/mcp/settings). An organization administrator can select **Edit access** to change permitted operations. Removing an operation also cancels its pending work; revoking the grant prevents the assistant from using the connection.

## Approve a change

1. Ask your assistant to prepare the change.
2. Open the Tross review link and check the target record, exact values and attachments.
3. Select **Approve and execute**, or deny the proposal.
4. Return to the assistant to retrieve the result and verify the change.

Preparing a proposal does not change the external system. Proposals expire after 15 minutes; edits require a new proposal. An assistant's confirmation message cannot approve a write.

If a write returns `outcome_unknown`, do not submit it again. Check the provider record with an authorized reviewer before deciding what to do next.

## Files and results

Upload files through the Tross upload page or the [developer example](../examples/tross-mcp/README.md). The assistant references an attachment ID; a local path alone does not upload a file. Uploads must match the declared filename, type and size, up to 50 MiB. Staged files expire after one hour.

Ask the assistant for the file's Tross download page, then sign in and select **Download file**. Agents can use the authenticated download API. File access follows the same connection permissions; a URL alone does not grant access.

For queued work, retrieve the existing run instead of submitting the action again. Use `next_offset` and deferred result paths to retrieve larger results. Results include their source and run reference.

## Sandbox

The sandbox uses isolated demo records and has no production provider access. Approved changes appear in subsequent reads within the same session. Customer connections require production sign-in and explicit access.
