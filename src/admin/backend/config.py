import environs

env = environs.Env()
env.read_env()

_DEV_SERVER             = "http://0.0.0.0:1234"
PUBLIC_URL              = env.str("PUBLIC_URL", "http://0.0.0.0:8080")

PROJECT_HOME_ADDRESS    = env.str("PROJECT_HOME_ADDRESS",    "Hausmanns gate 3, 0186 Oslo")

STATIC_URL              = env.str("STATIC_URL",              _DEV_SERVER)
STATIC_VERSION          = env.str("STATIC_VERSION",          "latest") if STATIC_URL != _DEV_SERVER else ""

API_URL                 = env.str("API_URL",                 "http://api")
SCHEDULER_URL           = env.str("SCHEDULER_URL",           "http://schedule")

PREDICTIONS_API_PATH    = env.str("PREDICTIONS_API_PATH",    "shapes")
USERS_API_PATH          = env.str("USERS_API_PATH",          "users")
COUNTRIES_API_PATH      = env.str("COUNTRIES_API_PATH",      "countries")

REDIS_CACHE_HOST        = env.str("REDIS_CACHE_HOST",        "0.0.0.0")
REDIS_CACHE_PORT        = env.int("REDIS_CACHE_PORT",        6379)
REDIS_CACHE_DB          = env.int("REDIS_CACHE_DB",          0)
REDIS_CACHE_EXPIRY_TIME = env.int("REDIS_CACHE_EXPIRY_TIME", 120)


EMAIL_FROM_ADDRESS      = env.str("EMAIL_FROM_ADDRESS",      "conflictcartographer@prio.org")
EMAIL_FROM_NAME         = env.str("EMAIL_FROM_NAME",         "The Conflict Cartographer Team")

EMAIL_COOLDOWN          = env.int("EMAIL_COOLDOWN",          31)

MAILJET_API_KEY         = env.str("MAILJET_API_KEY",         "000-000-000-000")
MAILJET_API_SECRET      = env.str("MAILJET_API_SECRET",      "000-000-000-000")
MAILJET_URL             = env.str("MAILJET_URL",             "https://api.mailjet.com")

LOG_LEVEL               = env.str("LOG_LEVEL",               "WARNING")

PARTICIPATION_LINK      = env.str("PARTICIPATION_LINK",      "https://conflictcartographer.prio.org")

LINKS = {
        "Project page": "https://www.prio.org/projects/1900",
        "Participate here": "https://conflictcartographer.prio.org/",
        "Tutorial video": "https://vimeo.com/665181134",
        "Source code": "https://github.com/prio-data/conflictcartographer",
    }
