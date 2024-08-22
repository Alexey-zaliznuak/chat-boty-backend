from os import getenv as env
from dotenv import load_dotenv


load_dotenv(override=True)


class NotProvided: ...

# TODO use configs libs
class BaseConfig:
    DATABASE_URL: str = ...

    POSTGRES_DB: str =...
    POSTGRES_USER: str = ...
    POSTGRES_PASSWORD: str = ...
    POSTGRES_HOST: str = ...
    POSTGRES_PORT: str = ...

    LOGGING_BASE_DIR: str = "logs"

    ARTIFACT_DIRECTORY: str = "data"
    STATIC_DIRECTORY: str = "static"

    AUTHORIZATION_KEY: str = ...

    TELEGRAM_BOT_TOKEN: str = ...
    TELEGRAM_ADMIN_CHAT_ID: str = ...

    def __init__(self) -> None:
        for env_variable_config_name in [attr for attr in self.__dir__() if not attr.startswith("__")]:
            value = self.__getattribute__(env_variable_config_name)

            if value is ...:
                value = env(env_variable_config_name, NotProvided)
                self.__setattr__(env_variable_config_name, value)

            if value is NotProvided:
                raise EnvironmentError(f"{env_variable_config_name} have not provided environment value")

Config = BaseConfig()
