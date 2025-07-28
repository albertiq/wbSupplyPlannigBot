from aiohttp import ClientSession, TCPConnector
from pydantic import AnyHttpUrl


class AsyncBaseHttpClient:
    def __init__(self, base_url: AnyHttpUrl, token: str | None = None):
        self.base_url = base_url
        self.headers = {"Authorization": f"{token}"}

    async def get(self, endpoint: str, params: dict = None) -> dict:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(f"{self.base_url}{endpoint}", params=params, headers=self.headers) as response:
                response.raise_for_status()

                return await response.json()

    async def post(self, endpoint: str, params: dict = None, data: dict | None = None) -> any:
        async with ClientSession() as session:
            async with session.post(url=f"{self.base_url}{endpoint}", params=params, json=data) as response:
                response.raise_for_status()

                return await response.json()
