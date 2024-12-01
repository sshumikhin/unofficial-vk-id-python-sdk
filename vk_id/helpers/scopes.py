from ..constants import Scopes
from ..exception import WrongScopes

# __all__ = []


class ValidateScopes:

    @staticmethod
    def check_scopes(value):
        if not type(value) == list:
            raise ValueError("Scopes must be a list of Scopes")

        if not set(value).issubset(Scopes):
            raise WrongScopes

        return ' '.join(value)

    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return getattr(instance, f"_{owner.__name__}__{self.name}")

    def __set__(self, instance, value):
        if getattr(instance, f"_{instance.__class__.__name__}__{self.name}", False):
            raise ValueError("Scopes already generated")
        value = self.check_scopes(value)
        setattr(instance, f"_{instance.__class__.__name__}__{self.name}", value)

    def __delete__(self, instance):
        pass