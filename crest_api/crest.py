from httpx import AsyncClient, HTTPStatusError
from .crest_url import CRestWebhookUrl
from .crest_limits_manager import CRestLimitsManager
from .utils import format_params, format_batch


class CRest:
    limits_manager = CRestLimitsManager()

    def __init__(
            self,
            domain: str,
            format,
            auth,
            max_batch_size: int = 50
    ) -> None:
        self.DOMAIN = domain
        self.FORMAT = format
        self.MAX_BATCH_SIZE = max_batch_size

    @limits_manager
    async def call(self, method: str, format: str, params: dict):
        url = CRestWebhookUrl(
            domain=self.DOMAIN,
            method=method,
            format=format
        ).get_url()

        async with AsyncClient() as client:
            response = await client.get(
                url=url,
                params=str(format_params(params)),
            )
            print(response.url)
            return response.json()

    @limits_manager
    async def batch_call(self, calls: list):
        results = []
        url = CRestWebhookUrl(
            domain=self.DOMAIN,
            format=self.FORMAT
        ).get_batch_url()
        print(url)

        for i in range(0, len(calls), self.MAX_BATCH_SIZE):
            batch_calls = calls[i:i + self.MAX_BATCH_SIZE]
            batch_params = format_batch(batch_calls)

            async with AsyncClient() as client:
                try:
                    response = await client.get(url=url, params=batch_params)
                    results.extend(response.json())
                    print(response.json())
                except HTTPStatusError as e:
                    print(f"HTTP error: {e}")
                except Exception as e:
                    print(f"An error: {e}")

        return results
