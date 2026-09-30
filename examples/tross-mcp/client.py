"""Public example: discovery, reads, proposals, polling, and attachments.

Install: pip install 'mcp>=1.30,<2' httpx
The hosted implementation is private; this example contains no provider code.
"""

import argparse
import asyncio
import json
import os
import uuid
from pathlib import Path
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def call(session, name, **kwargs):
    result = await session.call_tool(name, kwargs)
    if result.isError:
        raise RuntimeError(result.content)
    return result.structuredContent or json.loads(result.content[0].text)


async def connection_headers(url):
    # A production credential must never follow the example's sandbox default.
    if url.endswith("/sandbox/mcp"):
        token = os.getenv("TROSS_SANDBOX_TOKEN")
        if token:
            return {"x-tross-sandbox-token": token}
        async with httpx.AsyncClient(timeout=30) as bootstrap:
            response = await bootstrap.post(
                url.removesuffix("/mcp") + "/api/sessions"
            )
            response.raise_for_status()
            token = response.json()["token"]
        return {"x-tross-sandbox-token": token}
    token = os.getenv("TROSS_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("Set TROSS_ACCESS_TOKEN to your resource-bound OAuth token.")
    return {"Authorization": "Bearer " + token}


async def main(args):
    headers = await connection_headers(args.url)
    async with httpx.AsyncClient(headers=headers, timeout=60) as http:
        async with streamable_http_client(args.url, http_client=http) as (
            read,
            write,
            _,
        ):
            async with ClientSession(read, write) as session:
                await session.initialize()
                if not args.operation:
                    print(
                        json.dumps(
                            await call(session, "tross_list_connections"), indent=2
                        )
                    )
                    print(
                        json.dumps(
                            await call(
                                session, "tross_search_operations", query=args.query
                            ),
                            indent=2,
                        )
                    )
                    return
                contract = await call(
                    session, "tross_get_operation", operation_id=args.operation
                )
                if not args.input:
                    print(json.dumps(contract, indent=2))
                    return
                data = json.loads(Path(args.input).read_text())
                attachments = []
                if args.file:
                    import mimetypes

                    file = Path(args.file)
                    upload = await call(
                        session,
                        "tross_create_upload",
                        connection_id=args.connection,
                        filename=file.name,
                        content_type=mimetypes.guess_type(file.name)[0]
                        or "application/octet-stream",
                        size_bytes=file.stat().st_size,
                    )
                    print("Upload in the Tross page:", upload["upload_page"])
                    response = await http.put(
                        upload["upload_url"],
                        content=file.read_bytes(),
                        headers={"Content-Type": upload["content_type"]},
                    )
                    response.raise_for_status()
                    attachments = [upload["attachment_id"]]
                args_dict = {
                    "operation_id": args.operation,
                    "connection_id": args.connection,
                    "input": data,
                    "idempotency_key": args.idempotency_key or str(uuid.uuid4()),
                }
                write = contract["effect"] == "write"
                if write:
                    args_dict["attachment_ids"] = attachments
                result = await call(
                    session,
                    "tross_prepare_write" if write else "tross_execute_read",
                    **args_dict,
                )
                print(json.dumps(result, indent=2))
                if write:
                    print(
                        "A human must review and approve in Tross:",
                        result.get("review_url"),
                    )
                for _ in range(180):
                    if result["status"] not in (
                        "queued",
                        "dispatching",
                        "pending_approval",
                    ):
                        break
                    await asyncio.sleep(5)
                    result = await call(
                        session, "tross_get_run", run_id=result["run_id"]
                    )
                print(json.dumps(result, indent=2))
                if result["status"] == "outcome_unknown":
                    raise RuntimeError(
                        "Do not retry this write. Reconcile it with an authorized reviewer."
                    )
                while result.get("next_offset") is not None:
                    result = await call(
                        session,
                        "tross_get_run",
                        run_id=result["run_id"],
                        offset=result["next_offset"],
                    )
                    print(json.dumps(result, indent=2))
                # For large nested results, use a returned deferred JSON Pointer
                # as result_path in tross_get_run. Text uses character offsets.


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="https://mcp.ontross.com/sandbox/mcp")
    p.add_argument("--query", default="chart preparation")
    p.add_argument("--operation")
    p.add_argument("--connection")
    p.add_argument("--input", help="Path to an input JSON file on YOUR machine")
    p.add_argument(
        "--file", help="Local file read by this client and uploaded as bytes"
    )
    p.add_argument(
        "--idempotency-key",
        help="Persist and reuse this key for retries of the identical request",
    )
    asyncio.run(main(p.parse_args()))
