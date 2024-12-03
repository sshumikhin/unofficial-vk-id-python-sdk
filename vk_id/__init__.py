from vk_id.constants import Scopes
from vk_id.dataclasses.error import Error
from vk_id.dataclasses.tokens import Tokens
from vk_id.dataclasses.user import User
from vk_id.exception import AppAlreadyInitialized, AppNotInitialized, URINotTrusted
from vk_id.app import VK_ID
from vk_id.helpers.pkce import PKCE

VK_ID_APP_INSTANCE: VK_ID | None = None

__version__ = "0.2.0"

__all__ = ("configure_app",
           "get_app_configuration",
           "generate_pkce",
           "exchange_code",
           "get_user_public_info",
           "refresh_access_token")


def configure_app(
        app_name: str,
        client_id: str,
        client_secret: str,
        client_access_key: str,
        **uris
):

    global VK_ID_APP_INSTANCE

    if VK_ID_APP_INSTANCE is not None:
        raise AppAlreadyInitialized

    vk = VK_ID(
        app_name=app_name,
        client_id=client_id,
        client_secret=client_secret,
        client_access_key=client_access_key
    )

    for tag, url in uris.items():
        setattr(vk.trusted_uris, tag, url)

    VK_ID_APP_INSTANCE = vk


def get_app_configuration() -> VK_ID:
    # TODO: проверять if ... else ...
    try:
        return VK_ID_APP_INSTANCE
    except AttributeError:
        pass


def generate_pkce(scopes: list = None) -> PKCE:
    pkce = PKCE([Scopes.DEFAULT.value] if scopes is None else scopes)
    return pkce


async def exchange_code(
            code_verifier: str,
            redirect_uri_tag: str,
            code: str,
            device_id: str,
            state: str
    ) -> Error | Tokens:

    try:
        redirect_uri = getattr(VK_ID_APP_INSTANCE.trusted_uris, redirect_uri_tag)
    except AttributeError:
        raise URINotTrusted

    try:
        return await VK_ID_APP_INSTANCE._code_exchanger(
            code_verifier=code_verifier,
            redirect_uri=redirect_uri,
            code=code,
            device_id=device_id,
            state=state
        )
    except AttributeError:
        raise AppNotInitialized


async def get_user_public_info(access_token: str) -> Error | User:
    try:
        return await VK_ID_APP_INSTANCE._user_info(access_token=access_token)
    except AttributeError:
        raise AppNotInitialized


async def refresh_access_token(
        refresh_token: str,
        device_id: str,
        state: str,
        scopes: list = None
) -> Error | Tokens:

    scopes = [Scopes.DEFAULT.value] if scopes is None else scopes

    try:
        return await VK_ID_APP_INSTANCE._token_refresher(
            refresh_token=refresh_token,
            device_id=device_id,
            state=state,
            scopes=scopes
        )
    except AttributeError:
        raise AppNotInitialized
