import base64
import hashlib
import random
import string
from datetime import datetime
from typing import List
from vk_id.helpers.scopes import ValidateScopes

__all__ = ["PKCE"]


class PrivatePKCEParam:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, f"_{owner.__name__}__{self.name}")

    def __set__(self, instance, value):

        if getattr(instance, f"_{instance.__class__.__name__}__{self.name}", False):
            raise ValueError("PKCE already generated")

        setattr(instance, f"_{instance.__class__.__name__}__{self.name}", value)


class PKCE:

    __ALLOWED_CODE_VERIFIER_CHARACTERS = string.ascii_letters + string.digits + '_-'
    __CODE_CHALLENGE_METHOD = "S256"
    scopes = ValidateScopes()
    state = PrivatePKCEParam()
    code_verifier = PrivatePKCEParam()
    code_challenge = PrivatePKCEParam()

    def __init__(self,
                 scopes: List[str]
                 ):

        self.scopes = scopes
        self.state = self.__generate_state()
        self.code_verifier = self.__generate_code_verifier()
        self.code_challenge = self.__generate_code_challenge(self.code_verifier)

    @classmethod
    def __generate_state(cls, length=16):
        characters = string.ascii_letters + string.digits
        state = ''.join(random.choice(characters) for _ in range(length))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        return f"{state}-{timestamp}"

    @classmethod
    def __generate_code_verifier(cls):
        length = random.randint(a=43, b=128)
        result_str = ''.join(random.choice(cls.__ALLOWED_CODE_VERIFIER_CHARACTERS) for _ in range(length))

        return result_str

    @classmethod
    def __generate_code_challenge(cls, code_verifier: str) -> str:
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')
        return code_challenge

    # def __setattr__(self, key, value):
    #     if key not in self.__dict__:
    #         raise AttributeError
    #     super().__setattr__(key, value)