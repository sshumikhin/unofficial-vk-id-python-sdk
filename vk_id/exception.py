class WrongScopes(Exception):
    def __init__(self, message="Non-existent scopes"):
        self.message = message
        super().__init__(self.message)


class AppAlreadyInitialized(Exception):
    def __init__(self, message="App already initialized"):
        self.message = message
        super().__init__(self.message)


class AppNotInitialized(Exception):
    def __init__(self, message="App not initialized"):
        self.message = message
        super().__init__(self.message)


class OnlyHTTPS(Exception):
    def __init__(self, message="Only HTTPS URL'S is allowed"):
        self.message = message
        super().__init__(self.message)


class URINotTrusted(Exception):
    def __init__(self, message="URI is not trusted"):
        self.message = message
        super().__init__(self.message)