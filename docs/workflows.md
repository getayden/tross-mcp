# Workflow examples

Ask your assistant to find the operation first. Tross returns its required inputs, available fields and whether it reads or writes. Supported workflows vary by connection; see the [capability directory](https://app.ontross.com/mcp/catalog).

These examples use demo patient and encounter `1001` on `demo-ecw`. [Connect to the sandbox](https://app.ontross.com/mcp/connect?mode=sandbox) to try them.

## Prepare a chart

> Prepare a chart brief for demo patient 1001, encounter 1001. Retrieve the patient context, notes and medications. Include the source operations and any missing information.

The assistant discovers the relevant reads, collects required identifiers and summarizes their results.

## Write back a note

> Read the HPI for demo patient 1001, encounter 1001. Prepare an update: “Patient reports an improving cough. No fever or shortness of breath.” Give me the Tross review link.

Review and approve in Tross. Then ask:

> Retrieve the action result and read the note again to verify the approved change.

## Investigate a claim

> Find the claim lookup operation for my payer connection. Tell me which identifiers you need, then retrieve the claim and explain the available service lines, financial fields and payer remarks.

Use identifiers from your own authorized workflow. Different payers return different fields; a missing field is not evidence of a denial.

## Complete an operational action

> Find the eCW operation for creating a telephone encounter. Ask me for the required patient, provider, facility, time and reason, then prepare it for review.

Approve the proposal in Tross, retrieve the result and read the encounter list to verify it. An attachment example is available in the [Python guide](../examples/tross-mcp/README.md).

[Watch these workflows in ChatGPT](demos.md).
