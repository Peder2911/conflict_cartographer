from fastapi import FastAPI

from .routers import users, shapes, countries, nonanswers, quarters, email_status

app = FastAPI()


app.include_router(users.router,      prefix    = "/users", tags = ["Users",])
app.include_router(email_status.router,   prefix = "/users", tags = ["Users",])
app.include_router(shapes.router,     prefix    = "/shapes", tags = ["Responses",])
app.include_router(countries.router,  prefix    = "/countries", tags = ["Countries",])
app.include_router(nonanswers.router, prefix    = "/nonanswers", tags = ["Responses",])
app.include_router(quarters.router,   prefix    = "/quarters", tags = ["Summaries",])
