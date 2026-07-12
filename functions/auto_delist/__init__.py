"""Timer-triggered auto-delist job (runs hourly).

Expires past-date ``use_by`` items and marks zero-stock items sold out.
"""

from __future__ import annotations

import logging

import azure.functions as func
from shared.db import session_scope
from shared.delist import run_auto_delist

logger = logging.getLogger("functions.auto_delist")


def main(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logger.warning("auto_delist timer is past due")
    with session_scope() as db:
        result = run_auto_delist(db)
    logger.info("auto_delist complete: expired=%s sold_out=%s", result["expired"], result["sold_out"])
