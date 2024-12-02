import logging

from .env_config import env_config

from . import base  # noqa: F401

logger = logging.getLogger(__name__)

env_badge = []

if env_config.ENVIROMENT == "production":
    from .production import *  # noqa: F403

    env_badge = ["Production", "danger"]
elif env_config.ENVIROMENT == "testing":
    from .testing import *  # noqa: F403

    env_badge = ["Testing", "info"]
elif env_config.ENVIROMENT == "local":
    from .local import *  # noqa: F403

    env_badge = ["Local", "success"]
else:
    from .development import *  # noqa: F403

    env_badge = ["Development", "warning"]


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return env_badge


logger.warning(f"\n\tUsing environment: {env_config.ENVIROMENT.capitalize()}\n")
