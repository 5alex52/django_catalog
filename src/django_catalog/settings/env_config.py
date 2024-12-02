import logging

from pydantic import ValidationError
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class EnvConfig(BaseSettings):
    POSTGRES_HOST: str = "mebeltut_base"
    POSTGRES_DB: str = "mebeltut"
    POSTGRES_USER: str = "mebeltut_user"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_PORT: int | str = 5432

    SECRET_DJANGO: str = "test"
    SECRET_AUTH: str = ""

    EMAIL_PASSWORD: str = ""
    EMAIL_USER: str = ""

    TECH_BOT_TOKEN: str = ""
    TECH_CHANNEL_ID: str = ""

    S3_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_REGION: str = ""
    S3_URL: str = ""

    ENVIROMENT: str = "testing"

    class Config:  # pylint: disable=R0903
        case_sensitive = True
        env_file = ".env"

    @classmethod
    def validate_env(cls):
        try:
            cls()
        except ValidationError as e:
            error_details = e.errors()
            missing_parameters = [error["loc"][0] for error in error_details]
            if missing_parameters:
                raise ValueError(
                    f"Missing parameters in .env file: {', '.join(missing_parameters)}"
                ) from e


env_config = EnvConfig()
env_config.validate_env()
