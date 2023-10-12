from fastapi import APIRouter
import starlette.responses as _responses

router = APIRouter()


@router.get("/")
async def root():
    return _responses.RedirectResponse("/redoc")
