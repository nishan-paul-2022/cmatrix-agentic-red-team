
import redis
import os

redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
print(f"Checking connection to {redis_url}")

try:
    r = redis.from_url(redis_url)
    r.ping()
    print("Redis connection successful")
except Exception as e:
    print(f"Redis connection failed: {e}")
