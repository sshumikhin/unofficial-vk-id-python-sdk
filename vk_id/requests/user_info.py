from vk_id.dataclasses.error import Error
from vk_id.dataclasses.user import User
from vk_id.constants import URLS, DEFAULT_HEADERS
from vk_id.requests._base import BaseForRequests

import aiohttp


__all__ = ["_GetUserPublicInfo"]


class _GetUserPublicInfo(BaseForRequests):

    async def __call__(self,
                       access_token: str) -> User | Error:
        async with aiohttp.ClientSession() as session:

            data = {
                "access_token": access_token,
                "client_id": self._application.client_id
            }

            async with session.post(
                    url=URLS.USER_INFO,
                    headers=DEFAULT_HEADERS,
                    data=data) as resp:
                response_body = await resp.json()

                if response_body.get("error", False):
                    return Error(**response_body)

                return User(**response_body["user"])