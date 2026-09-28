from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from backend.database import Base, engine
from backend.routes.auth import router as auth_router
from backend.routes.recommendations import (
    router as recommendations_router
)

from backend.models.user import User
from backend.models.recommendation import Recommendation


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="PocketSmart AI",
    description="AI-powered Home Budget Planning Assistant",
    version="1.0.0"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# Register API routes
app.include_router(auth_router)
app.include_router(recommendations_router)


# -----------------------------
# Website Pages
# -----------------------------

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request
        }
    )


@app.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


@app.get("/dashboard")
def dashboard_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request
        }
    )


@app.get("/home-planner")
def home_planner_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "request": request
        }
    )


@app.get("/home-recommendations")
def home_recommendations_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home_recommendations.html",
        context={
            "request": request
        }
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "application": "PocketSmart AI"
    }