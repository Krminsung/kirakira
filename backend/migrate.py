"""
Run database migration for credit system
"""
import asyncio
import sys
sys.path.append('/app')

from app.db.session import AsyncSessionLocal
from sqlalchemy import text

async def run_migration():
    async with AsyncSessionLocal() as session:
        # Read migration file
        with open('/app/database/migrations/001_add_credit_system.sql', 'r') as f:
            sql = f.read()
        
        # Split by statement and execute
        statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().upper().startswith('COMMIT')]
        
        for statement in statements:
            if statement:
                print(f"Executing: {statement[:100]}...")
                try:
                    await session.execute(text(statement))
                    await session.commit()
                    print("✓ Success")
                except Exception as e:
                    print(f"✗ Error: {e}")
                    # Continue with other statements
                    await session.rollback()
        
        print("\n✅ Migration completed!")

if __name__ == "__main__":
    asyncio.run(run_migration())
