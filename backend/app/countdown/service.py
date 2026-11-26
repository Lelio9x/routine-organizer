from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.countdown.models import Countdown
from app.countdown.schemas import CountdownResponse, CountdownUpdate


def _build_response(countdown: Countdown) -> CountdownResponse:
    target = date.fromisoformat(countdown.target_date)
    days_remaining = max(0, (target - date.today()).days)
    return CountdownResponse(
        id=countdown.id,
        title=countdown.title,
        target_date=countdown.target_date,
        days_remaining=days_remaining,
    )


def get_countdown(db: Session, user_id: int) -> CountdownResponse:
    countdown = db.query(Countdown).filter(Countdown.user_id == user_id).first()
    if not countdown:
        default_target = (date.today() + timedelta(days=30)).isoformat()
        countdown = Countdown(
            user_id=user_id,
            title="Until We Meet Again",
            target_date=default_target,
        )
        db.add(countdown)
        db.commit()
        db.refresh(countdown)
    return _build_response(countdown)


def update_countdown(db: Session, user_id: int, payload: CountdownUpdate) -> CountdownResponse:
    countdown = db.query(Countdown).filter(Countdown.user_id == user_id).first()
    if not countdown:
        countdown = Countdown(
            user_id=user_id,
            title=payload.title or "Until We Meet Again",
            target_date=payload.target_date,
        )
        db.add(countdown)
    else:
        countdown.target_date = payload.target_date
        if payload.title is not None:
            countdown.title = payload.title

    db.commit()
    db.refresh(countdown)
    return _build_response(countdown)