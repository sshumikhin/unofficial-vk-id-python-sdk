from vk_id.dataclasses.error import Error
from vk_id.dataclasses.tokens import Tokens
from vk_id.helpers.scopes import ValidateScopes
from vk_id.constants import GrantTypes, URLS, DEFAULT_HEADERS, Scopes
import aiohttp

from vk_id.requests._base import BaseForRequests

__all__ = ["_RefreshAccessToken"]


class _RefreshAccessToken(BaseForRequests):

    async def __call__(self,
                       refresh_token: str,
                       device_id: str,
                       state: str,
                       scopes: list) -> Tokens| Error:
        async with aiohttp.ClientSession() as session:

            scopes = ValidateScopes.check_scopes(value=scopes)

            data = {
                "grant_type": GrantTypes.REFRESH_TOKEN.value,
                "refresh_token": refresh_token,
                "client_id": self._application.client_id,
                "device_id": device_id,
                "state": state,
                "scope": scopes
            }

            async with session.post(
                    url=URLS.AUTH,
                    headers=DEFAULT_HEADERS,
                    data=data) as resp:
                response_body = await resp.json()

                if response_body.get("error", False):
                    return Error(**response_body)

                return Tokens(**response_body)