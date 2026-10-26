from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.router import api_router

# Initialize database schema tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## SWE3020B: Software Quality Assurance and Security – CAT 2 Project Evaluation
    
    ### Core Functional Scope:
    * **Identity & Access Management:** Granular Role-Based Access Control (RBAC).
    * **Transactional Core:** Mobile Money integration abstraction, real-time balance computation,
      append-only double-entry ledger.
    * **Credit Engine:** Dynamic borrowing limits (3x shares multiplier), guarantor commitment validation,
      amortization schedules, and late penalty rules.
    * **Audit & Immutability:** Tamper-evident forensic audit logging.
    
    ### Architecture & Principles:
    * **Layered Clean Architecture:** Controller-Service-Repository separation of concerns.
    * **SOLID Principles:** SRP, OCP (Payment strategy), LSP, ISP, DIP (FastAPI Depends).
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cross-Origin Resource Sharing (CORS) configuration for frontend integration (Figma / React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
