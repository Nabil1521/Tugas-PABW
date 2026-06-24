import asyncio
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
SERVICES = {
    "MS1": "http://127.0.0.1:5051",
    "MS2": "http://127.0.0.1:5052",
    "MS3": "http://127.0.0.1:5053",
}

app = FastAPI(title="PBL0903 API Gateway")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


async def fetch_cars(client: httpx.AsyncClient, service: str, q: str) -> list[dict]:
    response = await client.get(f"{SERVICES[service]}/cars", params={"q": q})
    response.raise_for_status()
    cars = response.json()
    for car in cars:
        source_service = car.get("source_service")
        car["service"] = source_service.upper() if source_service in {"ms1", "ms2", "ms3"} else service
    return cars


async def fetch_combined_cars(primary_service: str, q: str) -> list[dict]:
    paired_service = "MS3" if primary_service == "MS2" else "MS2"
    async with httpx.AsyncClient(timeout=5) as client:
        results = await asyncio.gather(
            fetch_cars(client, primary_service, q),
            fetch_cars(client, paired_service, q),
        )
    return [car for group in results for car in group]


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/gateway/ms1/cars")
async def ms1_cars(q: str = "") -> list[dict]:
    async with httpx.AsyncClient(timeout=5) as client:
        return await fetch_cars(client, "MS1", q)


@app.get("/gateway/ms2/cars")
async def ms2_cars(q: str = "") -> list[dict]:
    return await fetch_combined_cars("MS2", q)


@app.get("/gateway/ms3/cars")
async def ms3_cars(q: str = "") -> list[dict]:
    return await fetch_combined_cars("MS3", q)
