from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def status() -> dict:
    return {"chronos": "online"}
