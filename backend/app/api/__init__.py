# app/api/__init__.py
from fastapi import APIRouter

# Create a main API router
api_router = APIRouter()

__all__ = ["api_router"]
