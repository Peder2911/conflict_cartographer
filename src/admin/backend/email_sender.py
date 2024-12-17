
import datetime
import logging
import base64
from typing import Optional, Dict
import pydantic
from toolz import compose
from toolz.curried import do

from cc_backend_lib.email import emailer
from cc_backend_lib.clients import countries_client, users_client
from cc_backend_lib.async_either import AsyncEither

from cc_email_templates import call_to_action_email

logger = logging.getLogger(__name__)

class EmailSender():

    def __init__(
            self,
            backend:            emailer.Emailer,
            countries:          countries_client.CountriesClient,
            users:              users_client.UsersClient,
            participation_link: str,
            address:            str,
            sender:             str,
            email_cooldown:     int,
            links:              Optional[Dict[str, str]] = None,
            ):

        self._backend            = backend
        self._participation_link = participation_link
        self._address            = address
        self._sender             = sender
        self._countries_client   = countries
        self._users_client       = users
        self._cached_countries   = None
        self._links              = links if links is not None else {}
        self._email_cooldown     = email_cooldown

    async def _can_send_to(self, id: str) -> bool:
        profile = await self._users_client.detail(str(id))

        if profile.either(lambda e: e.http_code == 404, lambda _: False):
            return True
        elif error := profile.either(lambda e: e, lambda _: None):
            logger.critial(f"Internal error when querying user profile for {id}: {str(error)}")
            return False
        else:
            profile = profile.value

            if profile.has_unsubscribed:
                logger.debug(f"{id} had unsubscribed")

            outside_cooldown = True

            if profile.last_mailed is not None:
                days_since_last_email = (datetime.date.today() - profile.last_mailed).days
                outside_cooldown = (days_since_last_email > self._email_cooldown)

                if outside_cooldown:
                    logger.debug(f"{days_since_last_email} days since last email to {id}")
                else:
                    logger.debug(f"Not emailing {id}. Last emailed {days_since_last_email} days ago.")

            return (not profile.has_unsubscribed) and outside_cooldown

    async def _update_email_cooldown(self, id: str):
        await self._users_client.set_email_cooldown_status(id)

    async def _send(self, subject, to, text, html):
        pydantic.EmailStr(to)
        can_send = True

        id = await self._users_client.id_from_email(to)
        if (user_id := id.value) is not None:
            can_send &= await self._can_send_to(user_id.id)
            if can_send:
                await self._update_email_cooldown(user_id.id)
        else:
            logger.debug(f"Email {to} not registered. OK to email!")

        if can_send:
            logger.debug(f"Emailing {to}")
            self._backend.send(subject, to, text, html)

    async def send_call_to_action(self, to: str, content: str):

        text, html = await self.render_call_to_action(
                to,
                content)

        await self._send("Dear participant", to, text, html)

    async def render_call_to_action(self, to_user, content):

        if countries := await self._countries():
            content_below = "Countries available: " + ", ".join(countries)
        else:
            content_below = None

        unsub_link = await self._unsub_link(to_user)

        return call_to_action_email(
                "Conflict Cartographer",
                content,
                "Participate",
                self._participation_link,
                content_below      = content_below,
                unsub_link         = unsub_link,
                address            = self._address,
                sender             = self._sender,
                links              = self._links)

    async def _unsub_link(self, to_email):
        check = await self._users_client.id_from_email(to_email)

        if check.is_left():
            return None
        else:
            key = base64.b16encode(to_email.encode()).decode()
            return f"https://conflictcartographer.prio.org/api/unsubscribe?key={key}"

    async def _countries(self):
        if self._cached_countries is None:
            ctries = await self._countries_client.list(only_active = True)
            self._cached_countries = (ctries
                .then(lambda ctries: [c.name for c in ctries.countries])
                .then(sorted)
                .either(lambda _: [], lambda x:x))

        return self._cached_countries
