from os import getenv as env
from dotenv import load_dotenv


load_dotenv()


class NotProvided: ...

# TODO use configs libs
class BaseConfig:
    DATABASE_URL: str = ...

    DB_NAME: str = ...
    DB_USER: str = ...
    DB_PASSWORD: str = ...
    DB_HOST: str = ...
    DB_PORT: str = ...

    LOGGING_BASE_DIR: str = "logs"

    ARTIFACT_DIRECTORY: str = "data"
    STATIC_DIRECTORY: str = "static"

    AUTHORIZATION_KEY: str = ...

    def __init__(self) -> None:
        for env_variable_config_name in [attr for attr in self.__dir__() if not attr.startswith("__")]:
            value = self.__getattribute__(env_variable_config_name)

            if value is ...:
                value = env(env_variable_config_name, NotProvided)
                self.__setattr__(env_variable_config_name, value)

            if value is NotProvided:
                raise EnvironmentError(f"{env_variable_config_name} have not provided environment value")

Config = BaseConfig()
