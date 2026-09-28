# PocketSmart AI 🏠💰

PocketSmart AI is an AI-powered Home Budget Planning Assistant built with Python, FastAPI, SQLite, and Google Gemini.

It helps users create a practical home interior budget plan based on their total budget, home type, interior style, rooms, and requirements.

## ✨ Features

- 🔐 User Registration
- 🔑 User Login
- 🚪 Logout
- 📊 User Dashboard
- 🏠 Home Budget Planner
- 🤖 AI-powered Budget Recommendations
- 📜 Budget Recommendation History
- 🔒 JWT Authentication
- 🗄️ SQLite Database
- ⚡ FastAPI Backend
- 🎨 HTML/CSS Frontend

## 🏠 Home Budget Planner

Users can provide:

- Total Budget
- Home Type
- Interior Style
- Rooms / Areas
- Additional Requirements

PocketSmart AI generates a budget plan covering areas such as:

- Living Room
- Bedroom
- Kitchen
- Lighting & Electrical
- Furniture & Storage
- Decor & Finishing
- Contingency

The generated plan also includes money-saving tips.

> AI-generated amounts are approximate estimates. Actual costs may vary depending on materials, labour, location, home size, and design choices.

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- JWT Authentication
- Passlib
- Pydantic

### AI

- Google Gemini
- `google-genai` Python SDK

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

## 📁 Project Structure

```text
PocketSmart-AI/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── recommendation.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── recommendations.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── auth.py
│       ├── auth_dependency.py
│       └── gemini_service.py
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── home_planner.html
│   └── home_recommendations.html
│
├── .gitignore
├── README.md
└── .env