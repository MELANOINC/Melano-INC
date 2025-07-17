from fastapi import FastAPI
from .agents import hermes, ares, chronos, athena


app = FastAPI(title="MELANO INC")


app.include_router(hermes.router, prefix="/hermes", tags=["hermes"])
app.include_router(ares.router, prefix="/ares", tags=["ares"])
app.include_router(chronos.router, prefix="/chronos", tags=["chronos"])
app.include_router(athena.router, prefix="/athena", tags=["athena"])


@app.get("/")
def read_root() -> dict:
    return {"message": "MELANO INC API Online"}
