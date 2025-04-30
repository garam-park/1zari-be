import psycopg2
import redis

from config import settings
from config.settings.base import DATABASES

db_settings = settings.base.DATABASES["default"]
PG_CONFIG = {
    "database": db_settings["NAME"],
    "user": db_settings["USER"],
    "password": db_settings["PASSWORD"],
    "host": db_settings["HOST"],
    "port": db_settings["PORT"],
}


# 2. PostgreSQL 연결 및 데이터 가져오기
def fetch_regions():
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT city_name, district_name, emd_name, ST_AsText(geometry)
        FROM search_district;
    """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


REDIS_CONFIG = {"host": "localhost", "port": 6379, "decode_responses": True}


# Redis에 저장 (key: region:시:군구:읍면동, value: polygon WKT)
def save_regions_to_redis(regions):
    r = redis.StrictRedis(**REDIS_CONFIG)
    for city, district, town, polygon_wkt in regions:
        key = f"region:{city}:{district}:{town}"
        r.set(key, polygon_wkt, 3600)
        print(f"Saved {key}")


if __name__ == "__main__":
    regions = fetch_regions()
    save_regions_to_redis(regions)
    print("All regions uploaded to Redis.")


fetch_regions()
