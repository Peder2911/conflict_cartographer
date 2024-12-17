
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from cc_backend_lib import models
from .. import tables, dependencies

router = APIRouter()

@router.get("/{user_id}/email-subscription")
def get_email_subscription_status(
        user_id: int,
        session: Session = Depends(dependencies.database)) -> models.user.UserEmailStatus:
    data = (session
        .query(
            tables.users.c.id,
            tables.profile.c.unsubscribed.label("has_unsubscribed"))
        .join(tables.users)
        .where(tables.users.c.id == user_id)
        ).first()
    if data is not None:
        return models.user.UserEmailStatus(**data)
    else:
        return Response(status_code = 404)

@router.put("/{user_id}/email-subscription")
def put_email_subscription_status(
        user_id:                   int,
        email_subscription_status: models.user.EmailStatus,
        session:                   Session = Depends(dependencies.database)) -> models.user.UserEmailStatus:

    if session.query(tables.users).where(tables.users.c.id == user_id).first() is not None:
        expression = (tables.profile
                .update()
                .where(tables.users.c.id == user_id)
                .values(unsubscribed = email_subscription_status.has_unsubscribed))
        session.execute(expression)
        session.commit()
        return models.user.UserEmailStatus(id = user_id, **email_subscription_status.dict(), status_code = 204)
    else:
        return Response(status_code = 404)


@router.put("/{user_id}/last-emailed")
def update_last_mailed(
        user_id: int,
        last_mailed: models.user.EmailCooldownStatus,
        session: Session = Depends(dependencies.database),
        ) -> models.user.EmailCooldownStatus:

    if session.query(tables.users).where(tables.users.c.id == user_id).first() is not None:
        expression = (tables.profile
                .update()
                .where(tables.users.c.id == user_id)
                .values(last_mailed = last_mailed.last_mailed))
        session.execute(expression)
        session.commit()
        return last_mailed
    else:
        return Response(status_code = 404)
