from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, events, venues, categories, rsvps, reviews, notifications, wishlist, badges, invitations, dashboard

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(venues.router, prefix="/venues", tags=["venues"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(rsvps.router, prefix="/rsvps", tags=["rsvps"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])
api_router.include_router(badges.router, prefix="/badges", tags=["badges"])
api_router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
