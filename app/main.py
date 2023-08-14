from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.controllers import scheduling

app=FastAPI(docs_url="/api/docs", openapi_uri="docs/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    
)
app.include_router(scheduling.router)