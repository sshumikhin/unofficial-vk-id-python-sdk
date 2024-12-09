# Third party
import aiohttp

# First party
from vk_id.constants import (
    GrantTypes,
    URLS,
    DEFAULT_HEADERS,
)
from vk_id.dataclasses.error import Error
from vk_id.dataclasses.tokens import Tokens
from vk_id.requests._base import BaseForRequests


__all__ = ["_ExchangeCodeToToken"]


class _ExchangeCodeToToken(BaseForRequests):
    """
        Класс для обмена кода подтверждения на токены


        Подробнее: https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/api-integration/api-description#Poluchenie-cherez-kod-podtverzhdeniya
    """

    async def __call__(self,
                       code_verifier: str,
                       redirect_uri: str,
                       code: str,
                       device_id: str,
                       state: str) -> Tokens | Error:
        """
            Ассинхронный запрос для обмена device_id, code, state на пару токенов.
        """
        async with aiohttp.ClientSession() as session:

            data = {
                "grant_type": GrantTypes.AUTHORIZATION_CODE.value,
                "code_verifier": code_verifier,
                "redirect_uri": redirect_uri,
                "code": code,
                "client_id": self._application.client_id,
                "device_id": device_id,
                "state": state
            }

            async with session.post(
                    url=URLS.AUTH.value,
                    headers=DEFAULT_HEADERS,
                    data=data) as resp:
                response_body = await resp.json()

                if response_body.get("error", False):
                    return Error(**response_body)

                return Tokens(**response_body)
