from pathlib import Path
import sqlite3
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


SERVICE_PORTS = {
    "ms1": 5051,
    "ms2": 5052,
    "ms3": 5053,
}
SITE_A_OWNERS = {"ms1", "ms2"}


class CarIn(BaseModel):
    carname: Annotated[str, Field(min_length=1, max_length=100)]
    carbrand: Annotated[str, Field(min_length=1, max_length=100)]
    carmodel: Annotated[str, Field(min_length=1, max_length=100)]
    carprice: Annotated[str, Field(min_length=1, max_length=30)]
    description: Annotated[str, Field(max_length=200)] = ""


class Car(CarIn):
    id: int
    source_service: str = "local"
    source_id: int | None = None


def create_microservice(service_name: str, db_path: Path) -> FastAPI:
    app = FastAPI(title=f"{service_name} Cars Microservice")
    service_key = service_name.lower()
    read_owners = SITE_A_OWNERS if service_key in SITE_A_OWNERS else {service_key}
    write_owners = SITE_A_OWNERS if service_key == "ms2" else {service_key}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:8011", "http://localhost:8011"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def get_connection() -> sqlite3.Connection:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def row_to_car(row: sqlite3.Row) -> Car:
        return Car(
            id=row["id"],
            carname=row["carname"],
            carbrand=row["carbrand"],
            carmodel=row["carmodel"],
            carprice=row["carprice"],
            description=row["description"],
            source_service=row["source_service"],
            source_id=row["source_id"],
        )

    def ensure_database() -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tbcarsweb (
                    id INTEGER NOT NULL PRIMARY KEY,
                    carname TEXT NOT NULL,
                    carbrand TEXT NOT NULL,
                    carmodel TEXT NOT NULL,
                    carprice TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    source_service TEXT NOT NULL DEFAULT 'local',
                    source_id INTEGER,
                    UNIQUE(source_service, source_id)
                )
                """
            )
            conn.execute(
                "UPDATE tbcarsweb SET source_service = ? WHERE source_service = 'local'",
                (service_key,),
            )

    def normalize_owner(owner: str | None) -> str:
        return (owner or service_key).strip().lower()

    def is_local_owner(owner: str) -> bool:
        return owner in write_owners

    def local_owner_filter() -> tuple[str, list[str]]:
        owners = sorted(read_owners)
        placeholders = ", ".join("?" for _ in owners)
        return placeholders, owners

    def proxy_url(owner: str, car_id: int) -> str:
        target_service = "ms2" if owner in SITE_A_OWNERS else owner
        port = SERVICE_PORTS.get(target_service)
        if port is None:
            raise HTTPException(status_code=400, detail="Owner service tidak dikenal")
        return f"http://127.0.0.1:{port}/cars/{car_id}?owner={owner.upper()}"

    async def proxy_update(owner: str, car_id: int, car: CarIn) -> Car:
        import httpx

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.put(proxy_url(owner, car_id), json=car.model_dump())
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Proxy update gagal: {exc}") from exc
        return Car(**response.json())

    async def proxy_delete(owner: str, car_id: int) -> None:
        import httpx

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.delete(proxy_url(owner, car_id))
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Proxy delete gagal: {exc}") from exc

    @app.on_event("startup")
    def startup() -> None:
        ensure_database()

    @app.get("/")
    def server_ready() -> dict[str, str]:
        return {"message": f"{service_name} Server Ready"}

    @app.get("/cars", response_model=list[Car])
    def list_cars(q: str = Query(default="", max_length=100)) -> list[Car]:
        keyword = f"%{q.strip()}%"
        owner_placeholders, owners = local_owner_filter()
        with get_connection() as conn:
            if q.strip():
                rows = conn.execute(
                    f"""
                    SELECT id, carname, carbrand, carmodel, carprice, description,
                           source_service, source_id
                    FROM tbcarsweb
                    WHERE source_service IN ({owner_placeholders})
                      AND (carname LIKE ? OR carbrand LIKE ? OR carmodel LIKE ?)
                    ORDER BY id ASC
                    """,
                    (*owners, keyword, keyword, keyword),
                ).fetchall()
            else:
                rows = conn.execute(
                    f"""
                    SELECT id, carname, carbrand, carmodel, carprice, description,
                           source_service, source_id
                    FROM tbcarsweb
                    WHERE source_service IN ({owner_placeholders})
                    ORDER BY id ASC
                    """,
                    owners,
                ).fetchall()
        return [row_to_car(row) for row in rows]

    @app.post("/cars", response_model=Car, status_code=201)
    def create_car(car: CarIn) -> Car:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tbcarsweb (
                    carname, carbrand, carmodel, carprice, description, source_service, source_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    car.carname,
                    car.carbrand,
                    car.carmodel,
                    car.carprice,
                    car.description,
                    service_key,
                    None,
                ),
            )
            conn.commit()
            row = conn.execute(
                """
                SELECT id, carname, carbrand, carmodel, carprice, description,
                       source_service, source_id
                FROM tbcarsweb
                WHERE id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()
        return row_to_car(row)

    @app.put("/cars/{car_id}", response_model=Car)
    async def update_car(car_id: int, car: CarIn, owner: str | None = Query(None)) -> Car:
        owner_key = normalize_owner(owner)
        if not is_local_owner(owner_key):
            return await proxy_update(owner_key, car_id, car)

        with get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE tbcarsweb
                SET carname = ?, carbrand = ?, carmodel = ?, carprice = ?, description = ?
                WHERE id = ? AND source_service = ?
                """,
                (car.carname, car.carbrand, car.carmodel, car.carprice, car.description, car_id, owner_key),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Car not found")
            row = conn.execute(
                """
                SELECT id, carname, carbrand, carmodel, carprice, description,
                       source_service, source_id
                FROM tbcarsweb
                WHERE id = ?
                """,
                (car_id,),
            ).fetchone()
        return row_to_car(row)

    @app.delete("/cars/{car_id}", status_code=204)
    async def delete_car(car_id: int, owner: str | None = Query(None)) -> None:
        owner_key = normalize_owner(owner)
        if not is_local_owner(owner_key):
            await proxy_delete(owner_key, car_id)
            return

        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM tbcarsweb WHERE id = ? AND source_service = ?",
                (car_id, owner_key),
            )
            conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Car not found")

    return app
