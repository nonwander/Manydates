import environ

ROOT_DIR = environ.Path(__file__) - 4
APPS_DIR = ROOT_DIR.path('api')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    env_file = str(ROOT_DIR.path('.envs/.env.prod'))
    print(f'Loading : {env_file}')
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')
