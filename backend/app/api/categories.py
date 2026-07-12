"""Category taxonomy router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryOut]:
    rows = (
        db.query(Category).filter(Category.active.is_(True)).order_by(Category.name_en.asc()).all()
    )
    return [CategoryOut.model_validate(c) for c in rows]


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> CategoryOut:
    category = Category(name_ar=payload.name_ar, name_en=payload.name_en, slug=payload.slug)
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryOut.model_validate(category)
