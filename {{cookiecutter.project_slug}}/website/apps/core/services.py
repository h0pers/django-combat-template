from django.db import connection
from django_redis import get_redis_connection


class HealthService:
    @staticmethod
    def check_database() -> None:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

    @staticmethod
    def check_cache() -> None:
        get_redis_connection("default").ping()
