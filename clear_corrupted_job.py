#!/usr/bin/env python3
"""Clear corrupted job data from Redis."""

import redis
import os

# Connect to Redis result backend
redis_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
print(f"Connecting to Redis at {redis_url}")

r = redis.from_url(redis_url)

# The corrupted job ID
job_id = "a8177d55-88e7-482d-96a6-ef8683b16d5a"

# Celery stores results with this key pattern
key = f"celery-task-meta-{job_id}"

# Check if key exists
if r.exists(key):
    print(f"Found corrupted job {job_id}, deleting...")
    r.delete(key)
    print("Deleted successfully!")
else:
    print(f"Job {job_id} not found in Redis")

# List all task keys
print("\nAll task keys in Redis:")
for key in r.scan_iter("celery-task-meta-*"):
    print(f"  - {key.decode()}")
