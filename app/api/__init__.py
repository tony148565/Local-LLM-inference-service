# app/api/__init__.py

from .analyze import router_api as analyze_router
from .classify import router_api as classify_router
from .track2event import router_api as track2event_router

__all__ = [
    "analyze_router",
    "classify_router",
    "track2event_router",
]