
import base64
import binascii
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends
from cc_backend_lib import models
from .. import tables, dependencies

router = APIRouter()

@router.get("/")
def users(sess: Session = Depends(dependencies.database)) -> models.user.UserList:
    """
    user
    ====

    Get a list of all users.
    """
    query = sess.query(
            tables.users.c.id,
            tables.users.c.username.label("name"),
            tables.users.c.email)
    user_list = models.user.UserList(users = [models.user.UserListed(**row) for row in query.all()])
    return user_list

@router.get("/{user_id}")
def user(
        user_id:int,
        sess: Session = Depends(dependencies.database)
        ) -> models.user.UserDetail:
    """
    user
    ====

    Get lots of details about a user.
    """

    user_row = (sess
            .query(
                tables.users.c.id,
                tables.users.c.username.label("name"),
                tables.users.c.email,
                tables.users.c.date_joined,
                tables.users.c.last_login,
                tables.profile.c.meta.label("submitted_metadata"),
                tables.profile.c.waiver.label("has_signed_waiver"),
                tables.profile.c.unsubscribed.label("has_unsubscribed"),
                tables.profile.c.last_mailed)
            .join(tables.profile)
            .where(tables.users.c.id == user_id)
            .first())

    if user is not None:
        data = dict(user_row)

        assigned_countries = (sess
                .query(tables.countries.c.gwno)
                .join(tables.profile_countries)
                .join(tables.profile)
                .where(tables.profile.c.id == user_id))

        data["assigned_countries"] = [c for c,*_ in assigned_countries]
        return models.user.UserDetail(**data)
    else:
        return Response(status_code=404)

@router.get("/whois-email/{b16_email}")
def user_from_email(
        b16_email: str,
        sess: Session = Depends(dependencies.database)
        ) -> models.user.UserIdentification:
    """
    user_from_email
    ====

    Translate an email address to a user ID.
    """
    try:
        email = base64.b16decode(b16_email.encode()).decode()
    except binascii.Error:
        return Response(status_code = 400)
    else:
        user_row = (sess.query(tables.users.c.id).where(tables.users.c.email == email).first())
        if user_row is not None:
            return models.user.UserIdentification(**dict(user_row))
        else:
            return Response(status_code=404)
