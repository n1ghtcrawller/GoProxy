import httpx
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, delete
# from app.models.ss_link import SSLink
# from app.models.user import User


class SSGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.api_base_url = "https://127.0.0.1:8081/access-keys"

    async def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(verify=False)

    async def list_access_keys(self) -> list[dict]:
        async with self._client() as client:
            response = await client.get(self.api_base_url)
            response.raise_for_status()
            return response.json()

    async def create_access_key(self) -> dict:
        async with self._client() as client:
            response = await client.post(self.api_base_url)
            response.raise_for_status()
            return response.json()

    async def get_access_key(self, key_id: int) -> Optional[dict]:
        async with self._client() as client:
            url = f"{self.api_base_url}/{key_id}"
            response = await client.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()

    async def rename_access_key(self, key_id: int, name: str) -> dict:
        async with self._client() as client:
            url = f"{self.api_base_url}/{key_id}/name"
            response = await client.put(url, data={"name": name})
            response.raise_for_status()
            return response.json()

    async def delete_access_key(self, key_id: int) -> bool:
        async with self._client() as client:
            url = f"{self.api_base_url}/{key_id}"
            response = await client.delete(url)
            return response.status_code == 204

    async def set_data_limit(self, bytes_limit: int) -> dict:
        async with self._client() as client:
            url = "https://127.0.0.1:8081/server/access-key-data-limit"
            payload = {"limit": {"bytes": bytes_limit}}
            response = await client.put(url, json=payload)
            response.raise_for_status()
            return response.json()

    async def remove_data_limit(self) -> bool:
        async with self._client() as client:
            url = "https://127.0.0.1:8081/server/access-key-data-limit"
            response = await client.delete(url)
            return response.status_code == 204
