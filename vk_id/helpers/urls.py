from ..exception import OnlyHTTPS, URINotTrusted


class TrustedURIs:

    def __getattribute__(self, url_tag: str):
        try:
            url = object.__getattribute__(self, url_tag)
            return url
        except Exception as _:
            return URINotTrusted

    def __setattr__(self, url_tag: str, value: str):
        if not value.startswith("https://"):
            raise OnlyHTTPS
        object.__setattr__(self, url_tag, value)
