"""Idempotent seed data: category taxonomy and a bootstrap admin.

Run with:  python -m app.db.seed
Admin credentials come from env (SEED_ADMIN_EMAIL / SEED_ADMIN_PHONE / SEED_ADMIN_PASSWORD).
"""

from __future__ import annotations

import os

from app.core.logging import configure_logging, get_logger
from app.db.session import SessionLocal
from app.models.category import Category
from app.services import auth_service

logger = get_logger("app.seed")

_CATEGORIES: list[tuple[str, str, str]] = [
    ("بقالة", "Groceries", "groceries"),
    ("خضار وفواكه", "Fruits & Vegetables", "fruits-vegetables"),
    ("مخبوزات", "Bakery", "bakery"),
    ("لحوم", "Meat", "meat"),
    ("ألبان", "Dairy", "dairy"),
    ("مشروبات", "Beverages", "beverages"),
    ("منظفات", "Cleaning Supplies", "cleaning"),
    ("مصنع", "Factory", "factory"),
    ("أدوية", "Pharmacy", "pharmacy"),
    ("إلكترونيات", "Electronics", "electronics"),
]


def seed_categories() -> int:
    created = 0
    with SessionLocal() as db:
        for name_ar, name_en, slug in _CATEGORIES:
            exists = db.query(Category).filter(Category.slug == slug).first()
            if exists is None:
                db.add(Category(name_ar=name_ar, name_en=name_en, slug=slug))
                created += 1
        db.commit()
    return created


def seed_admin() -> None:
    email = os.getenv("SEED_ADMIN_EMAIL")
    phone = os.getenv("SEED_ADMIN_PHONE", "+963900000000")
    password = os.getenv("SEED_ADMIN_PASSWORD")
    if not email or not password:
        logger.info("admin_seed_skipped_no_env")
        return
    with SessionLocal() as db:
        auth_service.bootstrap_admin(db, email=email, phone=phone, password=password)
    logger.info("admin_seed_ok", extra={"extra_fields": {"email_domain": email.split("@")[-1]}})


def main() -> None:
    configure_logging("INFO")
    n = seed_categories()
    seed_admin()
    logger.info("seed_complete", extra={"extra_fields": {"categories_created": n}})


if __name__ == "__main__":
    main()
