from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

PORTFOLIO_URL = "https://avinash-verma.netlify.app/"
GITHUB_URL = "https://github.com/avi-verma-web"

PROFILE: dict[str, Any] = {
    "name": "Avinash Verma",
    "headline": "Full-stack developer (MEAN | MERN)",
    "portfolio": PORTFOLIO_URL,
    "github": GITHUB_URL,
    "summary": (
        "Software developer focused on scalable full-stack applications "
        "using modern frameworks and cloud-native architectures. The portfolio "
        "describes over 5 years of experience across frontend, backend, and cloud."
    ),
    "contact_email": "imavinashverma99@gmail.com",
    "source": PORTFOLIO_URL,
}

SKILLS = [
    "Angular", "React.js", "Node.js", "Express.js", "MongoDB",
    "PostgreSQL", "Redux", "TypeScript", "JavaScript", "HTML", "CSS",
    "SCSS", "Firebase", "Python", "Socket.IO", "Multer",
    "AWS EC2", "AWS S3", "AWS RDS", "CI/CD",
    "AI/LLM integration", "Prompt engineering", "Semantic search systems",
]

PROJECTS = [
    {
        "name": "MERN Expense Tracker",
        "description": (
            "Full-stack expense tracker with registration, login, income and "
            "expense management, category insights, JWT authentication, MongoDB, "
            "Chart.js, React, Vite, Redux Toolkit, React Query and Tailwind CSS."
        ),
        "live_url": "https://avi-mern-expense-tracker.netlify.app/",
        "source_url": "https://github.com/avi-verma-web/MERN_EXPENSE_Tracker-2025/tree/main",
    },
    {
        "name": "Gen AI SEO Generator",
        "description": (
            "AI-powered SEO keyword generator using Cohere GenAI, Firebase "
            "Google Sign-In, Firestore, React 19, TailwindCSS, Vite and Axios."
        ),
        "live_url": "https://avi-coheregen-ai-seo-generator.netlify.app/login",
        "source_url": "https://github.com/avi-verma-web/gen-ai-seo-generator",
    },
    {
        "name": "Chat Application",
        "description": (
            "Real-time chat application built with Socket.IO, Express, React "
            "Hooks and custom CSS."
        ),
        "live_url": "https://avinash-chat-app.netlify.app/",
        "source_url": "https://github.com/avi-verma-web/socket-chat-app-react-avi-frontend",
    },
    {
        "name": "Netflix UI",
        "description": (
            "Netflix-style UI built with React functional components, Context "
            "API and CSS Flexbox, hosted on Firebase."
        ),
        "live_url": "https://netflix-clone-359d3.web.app/",
        "source_url": "https://github.com/avi-verma-web/netflixclone-react",
    },
    {
        "name": "Search Engine",
        "description": (
            "React search-engine prototype using Google API, Context API, "
            "CSS Flexbox and Firebase hosting."
        ),
        "live_url": "https://avi--clone.web.app/",
        "source_url": "https://github.com/avi-verma-web/react-Search-engine",
    },
    {
        "name": "Redux Contact Book",
        "description": (
            "React contact-book application with CRUD operations, Redux and "
            "Bootstrap, deployed on Firebase."
        ),
        "live_url": "https://avi-redux-contactbook.web.app/",
        "source_url": "https://github.com/avi-verma-web/react-redux-contact-book",
    },
]

mcp = FastMCP("Avinash Verma Portfolio")


@mcp.tool()
def get_profile() -> dict[str, Any]:
    """Return Avinash Verma's public professional profile and portfolio links."""
    return PROFILE


@mcp.tool()
def get_skills() -> dict[str, Any]:
    """Return the technical skills listed on Avinash Verma's portfolio."""
    return {"skills": SKILLS, "source": PORTFOLIO_URL}


@mcp.tool()
def get_projects() -> dict[str, Any]:
    """Return portfolio projects with descriptions, live demos and source repositories."""
    return {"projects": PROJECTS, "source": PORTFOLIO_URL}


@mcp.tool()
def search_portfolio(query: str) -> dict[str, Any]:
    """Search public portfolio profile, skills and projects using keywords."""
    terms = [part.lower() for part in query.split() if part.strip()]
    if not terms:
        return {"query": query, "matches": []}

    records = [
        {"type": "profile", "data": PROFILE},
        {"type": "skills", "data": {"skills": SKILLS}},
        *[{"type": "project", "data": project} for project in PROJECTS],
    ]
    matches = []
    for record in records:
        haystack = str(record["data"]).lower()
        if all(term in haystack for term in terms):
            matches.append(record)
    return {"query": query, "matches": matches, "source": PORTFOLIO_URL}


app = FastAPI(title="Avinash Verma Portfolio MCP", version="1.0.0")
app.mount("/mcp", mcp.streamable_http_app())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "avinash-verma-portfolio-mcp"}


@app.get("/privacy")
def privacy() -> dict[str, str]:
    return {
        "title": "Privacy Policy",
        "policy": (
            "This public portfolio MCP is read-only. It returns professional "
            "information published on the portfolio website. It does not require "
            "account sign-in, request personal data from visitors, or store user "
            "queries. Requests may be processed by the hosting provider to operate "
            "and secure the service."
        ),
        "contact": "imavinashverma99@gmail.com",
    }


@app.get("/terms")
def terms() -> dict[str, str]:
    return {
        "title": "Terms of Use",
        "terms": (
            "This service provides public professional portfolio information "
            "for informational purposes. Information is provided as-is and may "
            "change. Project names and linked repositories remain the property "
            "of their respective owners. Do not use this service to harass, "
            "impersonate, or misrepresent the portfolio owner."
        ),
        "contact": "imavinashverma99@gmail.com",
    }
