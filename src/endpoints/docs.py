from fastapi import APIRouter
from fastapi.responses import RedirectResponse
router = APIRouter()


@router.get("/")
def get_docs():
    return RedirectResponse(url="/docs/")
