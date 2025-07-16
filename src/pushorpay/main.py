from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pushorpay.db import supabase_client
from pushorpay.scheduler import start_scheduler

# Create a FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="pushorpay/templates")
start_scheduler()  # Start background jobs immediately


# Create routes
@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(
    name: str = Form(...),
    github: str | None = Form(None),
    leetcode: str | None = Form(None),
    daily_fine: float = Form(...),
):
    supabase_client.table("users").insert(
        {"name": name, "github": github, "leetcode": leetcode, "daily_fine": daily_fine}
    ).execute()
    return RedirectResponse("/leaderboard", status_code=303)


@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request):
    # Select all users
    users = supabase_client.table("users").select("*").execute().data
    fines = [
        (
            user["name"],
            sum(
                item["fine_amount"]
                for item in supabase_client.table("checkins")
                .select("fine_amount")
                .eq("user_id", user["id"])
                .execute()
                .data
            ),
        )
        for user in users
    ]
    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            # Sort by fine amount, highest first
            "fines": sorted(fines, key=lambda x: -x[1]),
        },
    )
