from pathlib import Path

from microservice_common import create_microservice


BASE_DIR = Path(__file__).resolve().parent
app = create_microservice("MS1", BASE_DIR.parent / "DB-A.db")
