#!/usr/bin/env python3
"""
Test database connection
"""

import sys
import os
import sqlite3

print("🔍 Testing database connection...")

# Test SQLite connection directly
try:
    db_path = "app/contracts.db"
    if os.path.exists(db_path):
        print(f"✅ Database file exists: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if contract_types table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contract_types';")
        result = cursor.fetchone()
        
        if result:
            print("✅ contract_types table exists")
            
            # Get current contract types
            cursor.execute("SELECT id, name, description FROM contract_types ORDER BY id;")
            types = cursor.fetchall()
            
            print(f"📋 Current contract types ({len(types)}):")
            for type_data in types:
                print(f"  {type_data[0]}: {type_data[1]} - {type_data[2]}")
                
        else:
            print("❌ contract_types table does not exist")
            
        conn.close()
        
    else:
        print(f"❌ Database file not found: {db_path}")
        
except Exception as e:
    print(f"💥 Error: {e}")
    import traceback
    traceback.print_exc()
