from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Truncate all tables in the database (PostgreSQL only)"

    def handle(self, *args, **kwargs):
        cursor = connection.cursor()

        # Get all table names
        tables = connection.introspection.table_names()

        # Skip Django internal tables
        skip = ["django_migrations"]

        tables_to_truncate = [table for table in tables if table not in skip]

        if not tables_to_truncate:
            self.stdout.write(self.style.WARNING("No tables to truncate"))
            return
        
        # Build TRUNCATE SQL
        sql = "TRUNCATE TABLE {} RESTART IDENTITY CASCADE;".format(
            ", ".join(tables_to_truncate)
        )

        # Execute truncate
        cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS("All tables truncated successfully!"))
