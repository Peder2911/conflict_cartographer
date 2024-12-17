import datetime
import json
import logging
import asyncio
from operator import add
from typing import List

from toolz.functoolz import identity, curry
from fastapi import FastAPI, Response

from pymonad.either import Either, Right

from cc_backend_lib import dal
from cc_backend_lib.clients import predictions_client, users_client, scheduler_client, countries_client
from cc_backend_lib.models import emailer, user
from cc_backend_lib.errors import http_error
from cc_backend_lib.cache import cache, redis_cache, pydantic_serializer
from cc_backend_lib.email import mailjet_emailer
from cc_backend_lib.async_either import AsyncEither

from . import config, email_sender, models

logging.basicConfig(level = getattr(logging,config.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

app = FastAPI()

countries = countries_client.CountriesClient(config.API_URL, config.COUNTRIES_API_PATH)
users = users_client.UsersClient(config.API_URL, config.USERS_API_PATH)

cc_dal = dal.Dal(
        predictions = predictions_client.PredictionsClient(config.API_URL, config.PREDICTIONS_API_PATH),
        scheduler   = scheduler_client.SchedulerClient(config.SCHEDULER_URL),
        users       = users,
        countries   = countries)

ConfiguredRedisCache = curry(redis_cache.RedisCache,
        host         = config.REDIS_CACHE_HOST,
        port         = config.REDIS_CACHE_PORT,
        db           = config.REDIS_CACHE_DB,
        expiry_time  = config.REDIS_CACHE_EXPIRY_TIME)

email_client = email_sender.EmailSender(
        backend = mailjet_emailer.MailjetEmailer(
            from_address = config.EMAIL_FROM_ADDRESS,
            from_name    = config.EMAIL_FROM_NAME,
            api_key      = config.MAILJET_API_KEY,
            api_secret   = config.MAILJET_API_SECRET,
            api_url      = config.MAILJET_URL),
        countries          = countries,
        users              = users,
        participation_link = config.PARTICIPATION_LINK,
        address            = config.PROJECT_HOME_ADDRESS,
        sender             = config.EMAIL_FROM_NAME,
        links              = config.LINKS,
        email_cooldown     = config.EMAIL_COOLDOWN)

cache_with_redis = curry(cache.cache, ConfiguredRedisCache)

def error_response(error: http_error.HttpError):
    return Response(error.message, status_code = error.http_code)

@app.get("/api/participation/")
@cache_with_redis(curry(pydantic_serializer.PydanticSerializer,emailer.ParticipationSummary), lambda shift: shift < 0)
async def participation_summary(shift: int = -1) -> emailer.ParticipationSummary:
    """
    participation_summary
    =====================

    Get a participation summary for all countries. Shift is -1 by default, but
    can be specified with a query parameter.
    """

    summary = await cc_dal.participant_summary(shift = shift)
    return summary.either(error_response, identity)

@app.get("/api/participation/{country_id}/")
@cache_with_redis(curry(pydantic_serializer.PydanticSerializer,emailer.ParticipationSummary), lambda country_id, shift: shift < 0)
async def participation_country_summary(country_id: int, shift: int = -1) -> emailer.ParticipationSummary:
    """
    participation_country_summary
    =============================

    Get a participation summary for a country.
    """

    summary = await cc_dal.participant_summary(shift = shift, country_id = country_id)
    return summary.either(error_response, identity)

@app.post("/api/email/send/participants/")
async def send_emails(to_spec: emailer.ParticipationEmailSpecification):
    """
    send_emails
    ===========

    Dispatch emails to all users according to the posted specification.  The
    cc_backend_lib.models.emailer.EmailSpecification model contains a shift and
    a list of countries, which is used to fetch users that participated for
    those countries in that time-period.
    """

    participants = Right([])

    for country in to_spec.countries:
        country_participants = await cc_dal.participants(to_spec.shift, country)
        participants = (Either
            .apply(curry(add))
            .to_arguments(participants ,country_participants.then(lambda u: u.users)))

        if participants.is_left():
            break

    async def _send_email(user_list: List[user.UserListed]):
        coroutines = []
        for email in {u.email for u in user_list}:
            logger.info(f"Sending an email to {email}")
            coroutines.append(email_client.send_call_to_action(email, to_spec.content))
        await asyncio.gather(*coroutines)

    await AsyncEither.from_either(participants).async_then(_send_email)
    return Response(status_code=200)

@app.post("/api/email/send/single/")
async def send_single_email(to_user: emailer.SingleEmailSpecification):
    """
    send_emails
    ===========

    Dispatch emails to all users according to the posted specification.  The
    cc_backend_lib.models.emailer.EmailSpecification model contains a shift and
    a list of countries, which is used to fetch users that participated for
    those countries in that time-period.
    """

    await email_client.send_call_to_action(to_user.email, to_user.content)
    return Response(status_code=200)

@app.post("/api/email/preview/")
async def preview_single_email(to_user: emailer.SingleEmailSpecification):
    """
    send_emails
    ===========

    Dispatch emails to all users according to the posted specification.  The
    cc_backend_lib.models.emailer.EmailSpecification model contains a shift and
    a list of countries, which is used to fetch users that participated for
    those countries in that time-period.
    """

    _, html = await email_client.render_call_to_action(to_user.email, to_user.content)
    return Response(html, status_code=200)

@app.put("/api/email-status")
async def update_email_status(posted: models.EmailStatusAdminPost) -> models.EmailStatusAdminPost:

    id = await users.id_from_email(posted.email)
    if (id := id.value) is None:
        return Response(status_code = 404)

    if posted.clear_last_emailed:
        result = await users.set_email_cooldown_status(id.id, datetime.date(year = 1992, month = 11, day = 29))
        logger.debug(result)
    await users.set_email_subscription_status(id.id, posted.has_unsubscribed)
    return posted

@app.get("/")
def get_app():
    static_url = "/".join((config.STATIC_URL,config.STATIC_VERSION))

    data = json.dumps({
            "public_url":config.PUBLIC_URL
        })

    return Response(f"""
    <html>
        <head>
            <link rel="stylesheet" href="{static_url}/app.css">
            <link rel="preconnect" href="https://fonts.gstatic.com">
            <link href="https://fonts.googleapis.com/css2?family=Raleway&display=swap" rel="stylesheet">
        </head>
        <body>
            <div id="app"></div>
            <script id="data-from-backend" type="application/json">
                {data}
            </script>
            <script src="{static_url}/app.js"></script>
        </body>
    </html>
    """)
