# Неофициальная SDK для работы с VK ID на Python

---
## Описание
Сервис [VK ID](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/intro/start-page) имеет удобные SDK 
для интеграции на [Android](https://github.com/VKCOM/vkid-android-sdk), а также для [WEB](https://github.com/VKCOM/vkid-web-sdk).

Однако, мной не было найдено официальной SDK для работы с VK ID на языке Python. 
Поэтому и был написан данный простенький пакет, реализующий API сервиса.

SDK поможет вам быстро и удобно реализовать [схему обмена через SDK с обменом кода на бэкенде](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/start-integration/auth-flow-web#Cherez-SDK-s-obmenom-koda-na-bekende).

---

## Что реализовано?
- ✅ Выдача PKCE параметров
- ✅ Аутентификация посредством device_id, code, state
- ✅ Получение незамаскированной информации о пользователе
- ✅ Обновление пары access и refresh токенов посредством refresh token'а
- ❌ Получение замаскированной информации о пользователе
- ❌ Логаут пользователя
- ❌ Отзыв токена

---
## Установка
```
pip install https://github.com/sshumikhin/unofficial-vk-id-python-sdk/raw/master/dist/unofficial_vk_id_sdk-0.2.1.tar.gz
```

---
## Быстрый старт

1) #### Конфигурация VK ID приложения. Проверяйте вводимые данные, поскольку VK ID не предоставляет возможности проверить заранее, существует ли данный сервис.
```
from vk_id import configure_app as vk_id_app_configure


vk_id_app_configure(
    app_name=APP_NAME,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_access_key=CLIENT_ACCESS_KEY,
    my_first_redirect_tag=REDIRECT_URI_1
    my_second_redirect_tag=REDIRECT_URI_2    
)
```


2) #### Выдача PKCE параметров в формате JSON (Пример для фреймфорка FastAPI)
```
from fastapi.responses import JSONResponse
from fastapi import status
from vk_id import get_app_configuration, Scopes

@router.get(
    path="vk/id/pkce",
    summary="Получение PKCE параметров",
    response_class
)
async def get_pkce(
):

    app = get_app_configuration()

    pkce = generate_pkce(
        scopes=[Scopes.DEFAULT.value]
    )

    payload = {
        "vk_app_id": int(app.client_id),
        "redirect_url": app.my_first_redirect_tag, 
        "code_challenge": pkce.code_challenge,
        "code_verifier": pkce.code_verifier,
        "scope": pkce.scopes,
        "app_name": app.app_name
    }
    
    # Необходимо сохранить где-то сформированные параметры
    await redis_client.set(
        key=pkce.state,
        value=payload
    )

    payload["state"] = pkce.state

    del payload["code_verifier"]

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=payload
        )
```
Убедитесь, что app.my_first_redirect_tag ссылается на подконтрольный вам эндпоинт. 
Это необходимо, поскольку при успешной аутентификации пользователя перебросит на данный эндпоинт с параметрами **code, state, device_id**.

P.S. Клиентская SDK инициализирует объект VK ID через официальную библиотеку и устанавливает переданные данным хендлером данные.

3) #### Объявление хендлера для обработки переданных code, device_id и state
```
from vk_id import exchange_code

@router.get(
    path="/oauth2/token",
    status_code=status.HTTP_200_OK,
    response_class=RedirectResponse,
)
async def get_code_state_device_id(
        request: Request,
):
    authenticated_response = RedirectResponse("/")

    if bool(tokens.model_dump(exclude_none=True)):
        return authenticated_response

    state = request.query_params.get("state", False)
    code = request.query_params.get("code", False)
    device_id = request.query_params.get("device_id", False)

    if not(state and code and device_id):
        return authenticated_response

    vk_id_auth_params = await redis_client.connection.hgetall(state)

    if vk_id_auth_params is None:
        return authenticated_response

    tokens = await exchange_code(
            code_verifier=vk_id_auth_params["code_verifier"],
            redirect_uri_tag="profile",
            code=code,
            device_id=device_id,
            state=state
    )
    await redis_client.delete(state)

    if isinstance(tokens, ExchangeCodeError):
        return authenticated_response

    success_response = RedirectResponse("https://obmenyay-ru.ru/items/my")

    success_response.set_cookie(
        key=str(JWTTokens.ACCESS.value),
        value=tokens.access_token,
        httponly=True,
        secure=True,
        samesite="none",
        expires=tokens.expires_in
    )

    success_response.set_cookie(
        key=str(JWTTokens.REFRESH.value),
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        expires=432000
    )

    success_response.set_cookie(
        key="device_id",
        value=device_id,
        httponly=True,
        secure=True,
        samesite="none",
        expires=432000
    )

    success_response.set_cookie(
        key="state",
        value=state,
        httponly=True,
        secure=True,
        samesite="none",
        expires=432000
    )

    return success_response

```

В данном примере в пользовательский браузер устанавливаются http only cookies и после этого пользователь редиректится на нужную мне страницу.


4) #### Использование получения пользовательских данных как FastAPI Depends

Пример реализации Depends

```
async def get_tokens(request: Request) -> GetTokens:
    return GetTokens(
        access_token=request.cookies.get(str(JWTTokens.ACCESS.value)),
        refresh_token=request.cookies.get(str(JWTTokens.REFRESH.value)),
)


async def get_current_user(request: Request) -> User | RedirectResponse:

    tokens = await get_tokens(request)


    if not bool(tokens.model_dump(exclude_none=True)):
        raise UserIsNotAuthenticated

    if tokens.access_token is not None:
        vk_server_response = await get_user_public_info(
            access_token=tokens.access_token
        )

        if isinstance(vk_server_response, User):
            return vk_server_response

        else:
            # TODO: если не были найдены в кэше, делать запрос.
            raise UserIsNotAuthenticated

    else:
        raise UserIsNotAuthenticated

```

Пример использования:
```
@router.post(
    path="/files/upload",
    status_code=status.HTTP_200_OK)
async def append_item_endpoint(
        file: UploadFile = File(...),
        current_user: VKUser = Depends(get_current_user), # Depends
        session: AsyncSession = Depends(async_session),
        s3_client: S3Client = Depends(selectel),
        name: str = Form(None),
        description: Optional[str] = Form(None)
):
    pass
```
---
## Больше примеров использования
- [Обменяй.ру](https://github.com/sshumikhin/obmenyay.ru)