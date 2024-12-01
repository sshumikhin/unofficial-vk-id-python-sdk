import enum
from enum import StrEnum


class Scopes(StrEnum):
    DEFAULT = "vkid.personal_info"
    EMAIL = "email"
    PHONE = "phone"
    FRIENDS = "friends"
    WALL = "wall"
    GROUPS = "groups"
    STORIES = "stories"
    DOCS = "docs"
    PHOTOS = "photos"
    ADS = "ads"
    VIDEO = "video"
    STATUS = "status"
    MARKET = "market"
    PAGES = "pages"
    NOTIFICATIONS = "notifications"
    STATS = "stats"
    NOTES = "notes"


class URLS(StrEnum):
    AUTH = "https://id.vk.com/oauth2/auth"
    REVOKE_TOKEN = "https://id.vk.com/oauth2/revoke"
    LOGOUT = "https://id.vk.com/oauth2/logout"
    HIDDEN_USER_INFO = "https://id.vk.com/oauth2/public_info"
    USER_INFO = "https://id.vk.com/oauth2/user_info"


class GrantTypes(StrEnum):
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"


CONTENT_TYPE = "application/x-www-form-urlencoded"
DEFAULT_HEADERS = {"Content-Type": CONTENT_TYPE}