from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.modules.home.page import render_home_page

router = APIRouter(tags=["home"])


@router.get("/", response_class=HTMLResponse)
def home() -> str:
    return render_home_page()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
