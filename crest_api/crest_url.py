from pydantic import BaseModel, Field, ValidationError
from abc import ABC, abstractmethod


class TranportFormatData(BaseModel):
    format: str = Field(..., pattern='^(json|xml)$')


class CRestUrl(ABC):
    def __init__(self, domain: str, method: str = "", format: str = 'json') -> None:
        self._domain = domain.rstrip('/')
        self._format = format
        self._method = method.strip('/') if method else ""

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def method(self) -> str:
        return self._method

    @property
    def format(self) -> str:
        return self._format

    @abstractmethod
    def get_url(self) -> str:
        pass


class CRestWebhookUrl(CRestUrl):
    def __init__(self, domain: str, method: str = "", format: str = 'json') -> None:
        super().__init__(domain, method, format)

    def get_url(self) -> str:
        return f"{self.domain}/{self.method}.{self.format}"

    def get_batch_url(self) -> str:
        return f"{self.domain}/batch.{self.format}"


class CRestApplicationUrl(CRestUrl):
    def __init__(
            self,
            domain: str,
            method: str,
            auth,
            format: str | TranportFormatData = 'json',
    ) -> None:
        super().__init__(domain, method, format)
        # НА БУДУЩЕЕ
