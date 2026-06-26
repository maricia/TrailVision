import sys
from pathlib import Path

BASE_DIR = Path(r"I:\MTB_Video_Analytics")
sys.path.append(str(BASE_DIR))

from services.database_service import DatabaseService

db = DatabaseService()

ride_id = db.create_ride(
    ride_name="Test Ride",
    location="Test Trail",
    trail_name="Demo Loop",
    notes="Database service test"
)

print(f"Created ride_id: {ride_id}")

tables = db.list_tables()
print("Tables:")
for table in tables:
    print(f" - {table[0]}")