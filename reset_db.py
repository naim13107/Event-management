# reset_db.py
import os
import django
from django.db import connection

# ✅ Replace with your actual settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")

django.setup()

with connection.cursor() as cursor:
    cursor.execute("""
        DO $$ DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
    """)

print("✅ All tables dropped from Render database!")
