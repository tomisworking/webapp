#!/usr/bin/env python
"""
Script to migrate data from SQLite to PostgreSQL

Usage:
    1. Backup SQLite: python scripts/migrate_sqlite_to_postgres.py backup
    2. Export data: python scripts/migrate_sqlite_to_postgres.py export
    3. Switch to PostgreSQL in .env (set DATABASE_URL)
    4. Run migrations: python manage.py migrate
    5. Import data: python scripts/migrate_sqlite_to_postgres.py import
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command


def backup_sqlite():
    """Create backup of SQLite database"""
    print("🔒 Creating SQLite backup...")
    
    sqlite_path = Path('backend/db.sqlite3')
    if not sqlite_path.exists():
        print("❌ SQLite database not found!")
        return False
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(f'backups/db_backup_{timestamp}.sqlite3')
    backup_path.parent.mkdir(exist_ok=True)
    
    shutil.copy2(sqlite_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return True


def export_data():
    """Export data from SQLite to JSON"""
    print("📤 Exporting data from SQLite...")
    
    export_path = Path('backups/data_export.json')
    export_path.parent.mkdir(exist_ok=True)
    
    # Export all data except contenttypes and sessions
    with open(export_path, 'w') as f:
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--exclude=contenttypes',
            '--exclude=auth.Permission',
            '--exclude=sessions',
            '--indent=2',
            stdout=f
        )
    
    print(f"✅ Data exported to: {export_path}")
    return True


def import_data():
    """Import data to PostgreSQL"""
    print("📥 Importing data to PostgreSQL...")
    
    export_path = Path('backups/data_export.json')
    if not export_path.exists():
        print("❌ Export file not found! Run 'export' first.")
        return False
    
    try:
        call_command('loaddata', str(export_path))
        print("✅ Data imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'backup':
        backup_sqlite()
    elif command == 'export':
        if backup_sqlite():
            export_data()
    elif command == 'import':
        import_data()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()

