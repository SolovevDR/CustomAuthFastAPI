from fastapi import FastAPI

from auth.router import router as router_auth
from user.router import router as router_user
from exceptions.error_handler import add_exception_handler


app = FastAPI(title="Recommendation App")


app.include_router(router_auth)
app.include_router(router_user)

# add_exception_handler(app)


@app.get("/")
async def root():
    return
