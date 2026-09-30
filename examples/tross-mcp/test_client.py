"""Credential-boundary checks for the public example; no network requests."""
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import client


class ConnectionHeadersTest(unittest.IsolatedAsyncioTestCase):
    async def test_production_token_never_reaches_sandbox(self):
        http = AsyncMock()
        response = MagicMock()
        response.json.return_value = {"token": "demo-session"}
        http.post.return_value = response
        factory = MagicMock()
        factory.return_value.__aenter__ = AsyncMock(return_value=http)
        factory.return_value.__aexit__ = AsyncMock()
        with patch.dict(client.os.environ, {"TROSS_ACCESS_TOKEN": "production-secret"}, clear=True), patch.object(client.httpx, "AsyncClient", factory):
            headers = await client.connection_headers("https://mcp.ontross.com/sandbox/mcp")
        self.assertEqual(headers, {"x-tross-sandbox-token": "demo-session"})
        factory.assert_called_once_with(timeout=30)
        http.post.assert_awaited_once_with("https://mcp.ontross.com/sandbox/api/sessions")

    async def test_existing_sandbox_session_is_preserved(self):
        with patch.dict(client.os.environ, {"TROSS_ACCESS_TOKEN": "production-secret", "TROSS_SANDBOX_TOKEN": "demo-session"}, clear=True):
            headers = await client.connection_headers("https://mcp.ontross.com/sandbox/mcp")
        self.assertEqual(headers, {"x-tross-sandbox-token": "demo-session"})

    async def test_production_never_uses_sandbox_token(self):
        with patch.dict(client.os.environ, {"TROSS_SANDBOX_TOKEN": "demo-session"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "TROSS_ACCESS_TOKEN"):
                await client.connection_headers("https://mcp.ontross.com/mcp")

    async def test_production_uses_explicit_oauth_token(self):
        with patch.dict(client.os.environ, {"TROSS_ACCESS_TOKEN": "production-secret", "TROSS_SANDBOX_TOKEN": "demo-session"}, clear=True):
            headers = await client.connection_headers("https://mcp.ontross.com/mcp")
        self.assertEqual(headers, {"Authorization": "Bearer production-secret"})


if __name__ == "__main__":
    unittest.main()
