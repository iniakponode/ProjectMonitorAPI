from fastapi import FastAPI
from app.api import router as api_router
import os
import dotenv

dotenv.load_dotenv()
app = FastAPI(
    title="Project and contracts management API",
    description="This is an API that provides resource for the management of apps dealing with government projects "
                "management",
    version="1.0.0",
)

app.include_router(api_router)
