#!/usr/bin/env python3
"""
Script để dọn dẹp các file không cần thiết trong dự án
"""
import os
import shutil
from pathlib import Path

def cleanup_project():
    """Dọn dẹp các file không cần thiết"""
    
    # Danh sách file có thể xóa
    files_to_remove = [
        # Test files
        "test_contract_text.py",
        "test_upload.py", 
        "test_sqlserver_connection.py",
        "test_contract.txt",
        
        # SQL Server migration files (nếu không dùng SQL Server)
        "migrate_to_sqlserver.py",
        "sqlserver_setup.sql",
        "recreate_database_utf8.sql", 
        "fix_encoding_final.sql",
        "update_database_encoding.sql",
        "update_contract_types.sql",
        "MIGRATION_GUIDE.md",
        
        # Utility scripts (tùy chọn)
        "create_sample_data.py",
        "create_sample_tags.py",
        "fix_contract_types.py", 
        "update_contract_types.py",
    ]
    
    # Danh sách thư mục có thể xóa
    dirs_to_remove = [
        "app/__pycache__",
    ]
    
    print("🧹 Bắt đầu dọn dẹp dự án...")
    print("=" * 50)
    
    removed_files = []
    removed_dirs = []
    
    # Xóa files
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                removed_files.append(file_path)
                print(f"✅ Đã xóa file: {file_path}")
            except Exception as e:
                print(f"❌ Lỗi khi xóa {file_path}: {e}")
        else:
            print(f"⚠️  File không tồn tại: {file_path}")
    
    # Xóa directories
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                removed_dirs.append(dir_path)
                print(f"✅ Đã xóa thư mục: {dir_path}")
            except Exception as e:
                print(f"❌ Lỗi khi xóa {dir_path}: {e}")
        else:
            print(f"⚠️  Thư mục không tồn tại: {dir_path}")
    
    print("=" * 50)
    print(f"🎉 Hoàn thành! Đã xóa {len(removed_files)} files và {len(removed_dirs)} thư mục")
    
    if removed_files:
        print("\n📁 Files đã xóa:")
        for f in removed_files:
            print(f"  - {f}")
    
    if removed_dirs:
        print("\n📂 Thư mục đã xóa:")
        for d in removed_dirs:
            print(f"  - {d}")
    
    # Hiển thị kích thước tiết kiệm được (ước tính)
    print(f"\n💾 Ước tính tiết kiệm: ~{len(removed_files) * 10}KB")
    
    print("\n✨ Dự án đã được dọn dẹp!")
    print("📝 Lưu ý: Các file core của ứng dụng vẫn được giữ nguyên")

def show_files_to_remove():
    """Hiển thị danh sách file sẽ bị xóa để người dùng xem trước"""
    files_to_remove = [
        "test_contract_text.py",
        "test_upload.py", 
        "test_sqlserver_connection.py",
        "test_contract.txt",
        "migrate_to_sqlserver.py",
        "sqlserver_setup.sql",
        "recreate_database_utf8.sql", 
        "fix_encoding_final.sql",
        "update_database_encoding.sql",
        "update_contract_types.sql",
        "MIGRATION_GUIDE.md",
        "create_sample_data.py",
        "create_sample_tags.py",
        "fix_contract_types.py", 
        "update_contract_types.py",
    ]
    
    dirs_to_remove = [
        "app/__pycache__",
    ]
    
    print("📋 Danh sách file/thư mục sẽ bị xóa:")
    print("=" * 50)
    
    print("📄 Files:")
    for f in files_to_remove:
        status = "✅ Tồn tại" if os.path.exists(f) else "❌ Không tồn tại"
        print(f"  - {f} ({status})")
    
    print("\n📁 Thư mục:")
    for d in dirs_to_remove:
        status = "✅ Tồn tại" if os.path.exists(d) else "❌ Không tồn tại"
        print(f"  - {d} ({status})")

if __name__ == "__main__":
    print("🧹 Script dọn dẹp dự án SH_HopDong")
    print("=" * 50)
    
    choice = input("Bạn muốn:\n1. Xem danh sách file sẽ xóa\n2. Thực hiện dọn dẹp\nChọn (1/2): ")
    
    if choice == "1":
        show_files_to_remove()
    elif choice == "2":
        confirm = input("\n⚠️  Bạn có chắc chắn muốn xóa các file này? (y/N): ")
        if confirm.lower() in ['y', 'yes']:
            cleanup_project()
        else:
            print("❌ Đã hủy thao tác dọn dẹp")
    else:
        print("❌ Lựa chọn không hợp lệ")
