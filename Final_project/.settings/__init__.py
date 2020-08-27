from .base import *

env_name = os.getenv('ENV_NAME', 'local')

if env_name == 'prod':
    from .production import *
elif env_name == 'stage':
    from .stage import *
else:
    from .development import *