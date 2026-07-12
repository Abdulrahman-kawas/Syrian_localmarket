"""API routers aggregated under the versioned prefix."""

from fastapi import APIRouter, Depends

from app.api import (
    admin,
    auth,
    categories,
    chat,
    complaints,
    delivery,
    listings,
    maps,
    media,
    notifications,
    qr,
    reviews,
    search,
    sellers,
    users,
)
from app.core.rate_limit import default_rate_limit

# Global default rate limit applies to every route; auth adds a stricter one.
api_router = APIRouter(dependencies=[Depends(default_rate_limit)])

api_router.include_router(auth.router)
api_router.include_router(sellers.router)
api_router.include_router(categories.router)
api_router.include_router(listings.router)
api_router.include_router(qr.router)
api_router.include_router(search.router)
api_router.include_router(reviews.router)
api_router.include_router(complaints.router)
api_router.include_router(chat.router)
api_router.include_router(maps.router)
api_router.include_router(media.router)
api_router.include_router(notifications.router)
api_router.include_router(delivery.router)
api_router.include_router(users.router)
api_router.include_router(admin.router)

__all__ = ["api_router"]
