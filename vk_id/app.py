from vk_id.helpers.urls import TrustedURIs
from vk_id.helpers.credentials import String, ClientID
from vk_id.requests.auth import _ExchangeCodeToToken
from vk_id.requests.user_info import _GetUserPublicInfo
from vk_id.requests.refresh import _RefreshAccessToken


class VK_ID:

    client_id = ClientID()
    client_secret = String()
    client_access_key = String()

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            client_access_key: str
    ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.client_access_key = client_access_key
        self.trusted_uris = TrustedURIs()
        self.code_exchanger = _ExchangeCodeToToken(self)
        self.user_info = _GetUserPublicInfo(self)
        self.token_refresher = _RefreshAccessToken(self)