"""Timer-triggered proximity notification job (runs every 15 minutes).

Notifies registered devices about newly-listed nearby deals.
"""

from __future__ import annotations

import logging

import azure.functions as func
from shared.db import session_scope
from shared.proximity import run_proximity

logger = logging.getLogger("functions.proximity")


def main(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logger.warning("proximity timer is past due")
    with session_scope() as db:
        result = run_proximity(db)
    logger.info(
        "proximity complete: deals=%s notifications=%s",
        result.get("deals", 0),
        result.get("notifications", 0),
    )
