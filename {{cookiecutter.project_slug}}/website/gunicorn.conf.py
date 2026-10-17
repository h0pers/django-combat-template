import os

bind = f"0.0.0.0:{os.environ.get('GUNICORN_PORT', '8000')}"
workers = int(os.environ.get("GUNICORN_WORKERS", os.process_cpu_count() * 2 + 1))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# Restart workers periodically to limit memory leaks.
max_requests = 1000
max_requests_jitter = 100

# Docker's overlay filesystem can stall worker heartbeats.
worker_tmp_dir = "/dev/shm"

# Each worker must open its own database connection pool after fork.
preload_app = False
