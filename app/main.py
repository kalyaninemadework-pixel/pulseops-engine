from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.pipelines import router as pipeline_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.agent import router as agent_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description='Enterprise-Grade Asynchronous Data Processing Microservice with Autonomous GenAI Root-Cause Intelligence.',
    openapi_url=settings.API_V1_STR + '/openapi.json',
    docs_url='/docs',
    redoc_url='/redoc',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(pipeline_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(agent_router, prefix=settings.API_V1_STR)

@app.get('/', tags=['Root & Health'])
def root():
    return {
        'service': settings.PROJECT_NAME,
        'version': settings.VERSION,
        'docs': '/docs',
        'status': 'healthy'
    }

@app.get('/health', tags=['Root & Health'])
def health_check():
    return {'status': 'UP', 'database': 'connected'}
