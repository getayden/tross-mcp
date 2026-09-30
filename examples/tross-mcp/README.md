# Python examples

Run these commands from `examples/tross-mcp`. The default server is the hosted sandbox; no account is required.

```sh
python -m pip install 'mcp>=1.30,<2' httpx
python client.py --query 'patient notes'
python client.py --operation ecw/fetch-notes --connection demo-ecw --input inputs/read-notes.json
```

## Prepare a write

```sh
python client.py --operation ecw/write-hpi-notes --connection demo-ecw --input inputs/prepare-hpi.json
```

Open the returned review link, inspect the change and approve it in Tross. The client waits and retrieves the result. It cannot approve its own proposal. Reuse `--idempotency-key` for retries of the same request. If the result is `outcome_unknown`, check it with an authorized reviewer before trying again.

## Attach a file

```sh
python client.py --operation ezderm/upload-document --connection demo-ezderm --input inputs/upload-document.json --file synthetic.pdf
```

The example uploads the local file as bytes and includes its attachment ID in the proposal. The supplied PDF contains demo data. Review and approve the upload in Tross.

## Use your production connection

Obtain an access token through your client's OAuth flow and store it in `TROSS_ACCESS_TOKEN`. Request resource `https://mcp.ontross.com/mcp` with `tross:read` and, for proposals/uploads, `tross:write`. Then explicitly pass the production URL:

```sh
python client.py --url https://mcp.ontross.com/mcp --query 'patient notes'
```

Use the connection ID returned by `tross_list_connections` and inputs for your authorized records. Keep tokens out of prompts, logs and source control.

Sandbox calls ignore `TROSS_ACCESS_TOKEN`. To reuse a demo session, set `TROSS_SANDBOX_TOKEN` to its session token.

## Retrieve larger results

The example polls queued runs and follows top-level `next_offset` values. For deferred nested results, call `tross_get_run` with the returned `result_path` and offset. Use `tross_get_file` for file metadata, then download with the same authorized identity.
