import httpx
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession


class SSGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.server_url = "https://95.111.207.234:8081"
        self.api_base_url = f"{self.server_url}/TestApiPrefix"

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(verify=False)

    async def test_server(self) -> dict:
        async with self._client() as client:
            url = "https://95.111.207.234:8081/TestApiPrefix/server"
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def create_access_key(self) -> dict:
        async with self._client() as client:
            url = f"{self.api_base_url}/access-keys"
            response = await client.post(url)
            response.raise_for_status()
            return response.json()

    async def get_access_key(self, key_id: str) -> Optional[dict]:
        async with self._client() as client:
            url = f"{self.api_base_url}/access-keys/{key_id}"
            response = await client.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()

    async def rename_access_key(self, key_id: str, name: str) -> dict:
        async with self._client() as client:
            url = f"{self.api_base_url}/access-keys/{key_id}/name"
            response = await client.put(url, json={"name": name})
            response.raise_for_status()
            return response.json()

    async def delete_access_key(self, key_id: str) -> bool:
        async with self._client() as client:
            url = f"{self.api_base_url}/access-keys/{key_id}"
            response = await client.delete(url)
            return response.status_code == 204

    async def set_data_limit(self, bytes_limit: int) -> dict:
        async with self._client() as client:
            url = f"{self.api_base_url}/server/access-key-data-limit"
            payload = {"limit": {"bytes": bytes_limit}}
            response = await client.put(url, json=payload)
            response.raise_for_status()
            return response.json()

    async def remove_data_limit(self) -> bool:
        async with self._client() as client:
            url = f"{self.api_base_url}/server/access-key-data-limit"
            response = await client.delete(url)
            return response.status_code == 204
